from rest_framework import serializers
from transaction.models import Transaction, TransactionBookMapping


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('transaction_id', 'member_id', 'total_price', 'discount')


class TransactionBookMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionBookMapping
        fields = ('transaction_id', 'book_id', 'book_amount')


class BookOrderSerializer(serializers.Serializer):
    book_id = serializers.IntegerField(required=True)
    book_amount = serializers.IntegerField(required=True)


class BookTransactionSerializer(serializers.Serializer):
    total_price = serializers.IntegerField(default=0)
    redeem_cash = serializers.IntegerField(default=0)
    point_receive = serializers.IntegerField(default=0)
    books = BookOrderSerializer(many=True)
