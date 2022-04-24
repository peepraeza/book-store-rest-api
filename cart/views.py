from rest_framework import status
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.response import Response
from rest_framework.views import APIView

from book.models import Book
from cart.models import Cart
from cart.serializers import CartSerializer
from middleware.decorators import is_authentication
from utils.utils import get_member_admin_detail


class CartActionView(APIView):

    @is_authentication(allowed_role=['MEMBER'])
    def get(self, request):
        member = get_member_admin_detail(request)
        cart = Cart.objects.filter(member_id=member.member_id)
        cart_serializer = CartSerializer(cart, many=True)
        total_price = 0
        point_receive = 0
        total_amount = 0
        for c in cart:
            book = Book.objects.get(book_id=c.book_id_id)
            if c.book_amount > book.book_amount:
                raise ParseError('book_id: {} not enough amount for sell'.format(book.book_id))
            total_amount += c.book_amount
            total_price += book.book_price * c.book_amount
            point_receive += book.book_point * c.book_amount
        return Response({
            'books': cart_serializer.data,
            'total_price': total_price,
            'point_receive': point_receive,
            'amount': total_amount
        })

    @is_authentication(allowed_role=['MEMBER'])
    def post(self, request):
        member = get_member_admin_detail(request)
        cart_req = request.data
        cart_req['member_id'] = member.member_id
        cart = Cart.objects.filter(book_id=cart_req['book_id']).first()
        if cart is not None:
            raise ParseError('Book already in cart')
        cart_serializer = CartSerializer(data=cart_req)
        cart_serializer.is_valid(raise_exception=True)
        cart_serializer.save()
        return Response({'detail': 'Book Added in Cart'}, status=status.HTTP_201_CREATED)

    @is_authentication(allowed_role=['MEMBER'])
    def put(self, request):
        member = get_member_admin_detail(request)
        cart_req = request.data
        cart = Cart.objects.filter(book_id=cart_req['book_id'], member_id=member.member_id).first()
        if cart is None:
            raise NotFound('Not found book in cart')
        cart.book_amount = cart_req['book_amount']
        cart.save()
        return Response({'detail': 'Book Updated in Cart'})

    @is_authentication(allowed_role=['MEMBER'])
    def delete(self, request, book_id):
        member = get_member_admin_detail(request)
        cart = Cart.objects.filter(book_id=book_id, member_id=member.member_id).first()
        if cart is None:
            raise NotFound('Not found book in cart')
        cart.delete()
        return Response({'detail': 'Book Deleted in Cart'})


