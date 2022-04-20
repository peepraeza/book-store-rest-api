from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    book_name = models.CharField(max_length=100)
    book_author = models.CharField(max_length=100)
    book_price = models.IntegerField()
    book_point = models.IntegerField()
    book_amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)


class Member(models.Model):
    member_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='members', default="")
    member_name = models.CharField(max_length=100)
    member_point = models.IntegerField(default=0)
    member_phone = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)


class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    admin_name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)


class AppConfig(models.Model):
    app_config_id = models.AutoField(primary_key=True)
    app_config_group = models.CharField(max_length=100)
    app_config_key = models.CharField(max_length=100)
    app_config_value = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)


class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    member_id = models.ForeignKey(Member, db_column='member_id', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)


class TransactionBookMapping(models.Model):
    transaction_id = models.ForeignKey(Transaction, db_column='transaction_id', on_delete=models.CASCADE)
    book_id = models.ForeignKey(Book, db_column='book_id', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        unique_together = (('transaction_id', 'book_id'),)
