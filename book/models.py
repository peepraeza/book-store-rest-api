from django.db import models


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
