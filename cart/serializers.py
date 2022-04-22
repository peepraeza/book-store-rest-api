from rest_framework import serializers
from cart.models import Cart


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('member_id', 'book_id', 'book_amount')
        extra_kwargs = {
            'member_id': {'write_only': True}
        }





