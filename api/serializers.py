from rest_framework import serializers
from api.models import Book, Member, Admin, AppConfig, Transaction
from django.contrib.auth.models import User
from django.contrib.auth import password_validation


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('book_id', 'book_name', 'book_author', 'book_price', 'book_point', 'book_amount', 'created_at')


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['member_phone', 'member_point', 'user_id']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
