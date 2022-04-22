import jwt
from django.http import JsonResponse
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.response import Response
from rest_framework.views import APIView

from book.models import Book
from cart.models import Cart
from cart.serializers import CartSerializer
from middleware.decorators import is_authentication
from transaction.serializers import BookOrderSerializer
from user.models import Member
from utils.utils import get_member_admin_detail


class CartActionView(APIView):

    @is_authentication(allowed_role=['MEMBER'])
    def get(self, request):
        member = get_member_admin_detail(request)
        cart = Cart.objects.filter(member_id=member.member_id)
        cart_serializer = CartSerializer(cart, many=True)
        total_price = 0
        point_receive = 0
        for c in cart:
            book = Book.objects.get(book_id=c.book_id_id)
            total_price += book.book_price
            point_receive += book.book_point
        return Response({
            'books': cart_serializer.data,
            'total_price': total_price,
            'point_receive': point_receive
        })

    @is_authentication(allowed_role=['MEMBER'])
    def post(self, request):
        member = get_member_admin_detail(request)
        cart_req = request.data
        cart_req['member_id'] = member.member_id
        cart = Cart.objects.filter(book_id=cart_req['book_id']).first()
        if cart is not None:
            raise ParseError('book already in cart')

        cart_serializer = CartSerializer(data=cart_req)
        cart_serializer.is_valid(raise_exception=True)
        cart_serializer.save()
        return Response(cart_serializer.data)

    #
    # @is_authentication(allowed_role=['ADMIN'])
    # def put(self, request):
    #     book_data = request.data
    #     book = Book.objects.get(book_id=book_data['book_id'])
    #     book_serializer = BookSerializer(book, data=book_data)
    #     if book_serializer.is_valid():
    #         book_serializer.save()
    #         return JsonResponse("Updated Successfully", safe=False)
    #     return JsonResponse("Failed to Update")
    #
    # @is_authentication(allowed_role=['ADMIN'])
    # def delete(self, request, book_id):
    #     book = Book.objects.get(book_id=book_id)
    #     book.delete()
    #     return JsonResponse("Deleted Successfully", safe=False)


