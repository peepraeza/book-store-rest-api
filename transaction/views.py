from rest_framework.exceptions import NotFound, ParseError
from rest_framework.response import Response
from rest_framework.views import APIView

from appconfig.models import AppConfig
from book.models import Book
from middleware.decorators import is_authentication
from transaction.serializers import BookTransactionSerializer, TransactionSerializer, TransactionBookMappingSerializer
from utils.utils import get_member_admin_detail


class BookBuyView(APIView):

    @is_authentication(allowed_role=['MEMBER'])
    def post(self, request):

        req_body = request.data
        member = get_member_admin_detail(request)
        req_body['member_id'] = member.member_id

        book_transaction_serializer = BookTransactionSerializer(data=request.data)
        book_transaction_serializer.is_valid(raise_exception=True)
        if req_body['redeem_cash'] != 0:
            appconfig = AppConfig.objects.get(app_config_key='point_ratio')
            can_redeem = member.member_point / int(appconfig.app_config_value)
            used_point = req_body['redeem_cash'] * int(appconfig.app_config_value)
            if req_body['redeem_cash'] > can_redeem:
                raise ParseError('redeem_cash more than existed point')
            req_body['discount'] = req_body['redeem_cash']
            req_body['point_receive'] -= used_point

        transaction_serializer = TransactionSerializer(data=req_body)
        transaction_serializer.is_valid(raise_exception=True)
        transaction = transaction_serializer.save()

        for book_order in req_body['books']:
            try:
                book_id = book_order['book_id']
                book = Book.objects.get(book_id=book_id)
                book.book_amount = book.book_amount - book_order['book_amount']
                book.save()
                data = {'transaction_id': transaction.transaction_id, 'book_id': book_id,
                        'book_amount': book_order['book_amount']}
                transaction_book_mapping_serializer = TransactionBookMappingSerializer(data=data)
                transaction_book_mapping_serializer.is_valid(raise_exception=True)
                transaction_book_mapping_serializer.save()
            except Exception as e:
                raise Exception(e)

        member.member_point += req_body['point_receive']
        member.save()

        return Response({'data': 'success'})
