import datetime
import jwt

from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User


# Create your views here.
from user.serializers import UserSerializer, MemberSerializer, AdminSerializer


class MemberRegisterView(APIView):
    def post(self, request):
        # create user
        user_serializer = UserSerializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()

        # create member
        user_id = user_serializer.data['id']
        member_serializer = MemberSerializer(data=request.data)
        if member_serializer.is_valid():
            member_serializer.save(user_id=user_id)
        return Response(member_serializer.data)


class UserLoginView(APIView):
    def post(self, request):
        role = request.path.split('/')[2].upper()
        username = request.data['username']
        password = request.data['password']

        user = User.objects.filter(username=username).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow(),
            'role': role
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()

        response.data = {
            'token': token
        }
        return response


class MemberInfoView(APIView):

    def get(self, request):
        token = request.headers['Authorization']
        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except:
            print('error Authen')
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class AdminRegisterView(APIView):
    def post(self, request):
        # create user
        user_serializer = UserSerializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()

        # create member
        user_id = user_serializer.data['id']
        admin_serializer = AdminSerializer(data=request.data)
        if admin_serializer.is_valid():
            admin_serializer.save(user_id=user_id)
        return Response(admin_serializer.data)


class AdminInfoView(APIView):

    def get(self, request):
        token = request.headers['Authorization']
        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)