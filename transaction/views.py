import math
from rest_framework import status
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.response import Response
from rest_framework.views import APIView

from appconfig.models import AppConfig
from book.models import Book
from cart.models import Cart
from middleware.decorators import is_authentication
from transaction.models import Transaction
from transaction.serializers import BookOrderReqSerializer, TransactionSerializer, TransactionBookMappingSerializer
from utils.utils import get_member_admin_detail


class BookOrderView(APIView):

    @is_authentication(allowed_role=['MEMBER'])
    def post(self, request):

        member = get_member_admin_detail(request)
        book_order_req_serializer = BookOrderReqSerializer(data=request.data)
        book_order_req_serializer.is_valid(raise_exception=True)

        redeem_point = book_order_req_serializer.data['redeem_point']
        discount_cash = 0
        if redeem_point > 0:
            if redeem_point > member.member_point:
                raise ParseError('redeem point more than exist member point.')
            app_config = AppConfig.objects.filter(app_config_key='point_ratio').first()
            if app_config is None:
                raise NotFound('not found key point_ratio in app config')
            point_ratio = int(app_config.app_config_value)
            if redeem_point < point_ratio:
                raise ParseError('unable to redeem')
            discount_cash = redeem_point / point_ratio
        carts = Cart.objects.filter(member_id=member.member_id)
        transaction_serializer = TransactionSerializer(data={'member_id': member.member_id})
        transaction_serializer.is_valid(raise_exception=True)
        transaction = transaction_serializer.save()
        transaction_id = transaction.transaction_id

        total_price = 0
        point_receive = 0
        for book_order in carts:
            try:
                book_id = book_order.book_id_id
                book = Book.objects.get(book_id=book_id)
                book.book_amount = book.book_amount - book_order.book_amount
                total_price += book.book_price * book_order.book_amount
                point_receive += book.book_point * book_order.book_amount
                book.save()
                data = {'transaction_id': transaction_id, 'book_id': book_id,
                        'book_amount': book_order.book_amount}
                transaction_book_mapping_serializer = TransactionBookMappingSerializer(data=data)
                transaction_book_mapping_serializer.is_valid(raise_exception=True)
                transaction_book_mapping_serializer.save()
            except Exception as e:
                raise Exception(e)

        transaction.total_price = total_price
        transaction.discount = math.floor(discount_cash)
        transaction.save()

        member.member_point += point_receive - redeem_point
        member.save()
        carts.delete()
        return Response({'detail': 'Order Created Successfully'}, status=status.HTTP_201_CREATED)


class TransactionHistoryView(APIView):
    @is_authentication(allowed_role=['ADMIN'])
    def get(self, request):
        start_at = request.query_params.get('start_at', '1999-01-01')
        end_at = request.query_params.get('end_at', '3000-01-01')
        qs = Transaction.objects.filter(created_at__gte=start_at, created_at__lte=end_at)
        transactions = TransactionSerializer(qs, many=True).data

        return Response({'transactions': transactions})
