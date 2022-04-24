from django.db import models
from book.models import Book
from user.models import Member


class Cart(models.Model):
    member_id = models.ForeignKey(Member, db_column='member_id', on_delete=models.CASCADE)
    book_id = models.ForeignKey(Book, db_column='book_id', on_delete=models.CASCADE)
    book_amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        unique_together = (('member_id', 'book_id'),)