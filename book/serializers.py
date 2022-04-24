from rest_framework import serializers
from book.models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('book_id', 'book_name', 'book_author', 'book_price', 'book_point', 'book_amount')



