from rest_framework import serializers
from transaction.models import Transaction, TransactionBookMapping


class TransactionBookMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionBookMapping
        fields = ('transaction_id', 'book_id', 'book_amount')
        extra_kwargs = {
            'transaction_id': {'write_only': True}
        }


class TransactionSerializer(serializers.ModelSerializer):
    books = TransactionBookMappingSerializer(many=True, read_only=True)

    class Meta:
        model = Transaction
        fields = ['transaction_id', 'member_id', 'total_price', 'discount', 'created_at', 'books']


class BookOrderReqSerializer(serializers.Serializer):
    redeem_point = serializers.IntegerField(required=True)
