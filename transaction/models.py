from django.db import models

from user.models import Member
from book.models import Book


# Create your models here.
class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    member_id = models.ForeignKey(Member, db_column='member_id', on_delete=models.CASCADE)
    total_price = models.IntegerField(default=0)
    discount = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)


class TransactionBookMapping(models.Model):
    transaction_id = models.ForeignKey(Transaction, db_column='transaction_id', on_delete=models.CASCADE)
    book_id = models.ForeignKey(Book, db_column='book_id', on_delete=models.CASCADE)
    book_amount = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        unique_together = (('transaction_id', 'book_id'),)