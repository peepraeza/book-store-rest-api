from django.http import JsonResponse
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from book.models import Book
from book.serializers import BookSerializer

# Create your views here.
from middleware.decorators import is_authentication


class BookActionView(APIView):

    def get(self, request):
        print('get all book')
        books = Book.objects.filter(book_amount__gt=0)
        books_serializer = BookSerializer(books, many=True)
        return Response({'books': books_serializer.data})

    @is_authentication(allowed_role=['ADMIN'])
    def post(self, request):
        book_serializer = BookSerializer(data=request.data)
        book_serializer.is_valid(raise_exception=True)
        book_serializer.save()
        return Response({'detail': 'Book Created Successfully'}, status=status.HTTP_201_CREATED)

    @is_authentication(allowed_role=['ADMIN'])
    def put(self, request):
        book_data = request.data
        book = Book.objects.filter(book_id=book_data['book_id']).first()
        if book is None:
            raise NotFound('Book not found by given id')
        book_serializer = BookSerializer(book, data=book_data)
        book_serializer.is_valid(raise_exception=True)
        book_serializer.save()
        return Response({'detail': 'Book Updated Successfully'})

    @is_authentication(allowed_role=['ADMIN'])
    def delete(self, request, book_id):
        book = Book.objects.filter(book_id=book_id).first()
        if book is None:
            raise NotFound('Book not found by given id')
        book.delete()
        return Response({'detail': 'Book Deleted Successfully'})
