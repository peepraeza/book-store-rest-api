from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from book.models import Book
from book.serializers import BookSerializer


# Create your views here.
from middleware.decorators import is_authentication


class BookActionView(APIView):

    def get(self, request):
        print('get all book')
        books = Book.objects.all()
        books_serializer = BookSerializer(books, many=True)
        return JsonResponse(books_serializer.data, safe=False)

    @is_authentication(allowed_role=['ADMIN'])
    def post(self, request):
        book_serializer = BookSerializer(data=request.data)
        book_serializer.is_valid(raise_exception=True)
        book_serializer.save()
        return Response(book_serializer.data)

    @is_authentication(allowed_role=['ADMIN'])
    def put(self, request):
        book_data = request.data
        book = Book.objects.get(book_id=book_data['book_id'])
        book_serializer = BookSerializer(book, data=book_data)
        if book_serializer.is_valid():
            book_serializer.save()
            return JsonResponse("Updated Successfully", safe=False)
        return JsonResponse("Failed to Update")

    @is_authentication(allowed_role=['ADMIN'])
    def delete(self, request, book_id):
        book = Book.objects.get(book_id=book_id)
        book.delete()
        return JsonResponse("Deleted Successfully", safe=False)