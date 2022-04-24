import datetime
import jwt

from rest_framework.exceptions import AuthenticationFailed, NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.models import User

# Create your views here.
from appconfig.models import AppConfig
from middleware.decorators import is_authentication
from user.models import Member, Admin
from user.serializers import UserSerializer, MemberSerializer, AdminSerializer
from utils.utils import get_member_admin_detail


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
        return Response({'detail': 'Member Created Successfully'}, status=status.HTTP_201_CREATED)


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

        if role == 'MEMBER':
            try:
                Member.objects.get(user_id=user.id)
            except Exception as e:
                raise NotFound('User not found!')
        else:
            try:
                Admin.objects.get(user_id=user.id)
            except Exception as e:
                raise NotFound('User not found!')

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
    @is_authentication(allowed_role=['MEMBER'])
    def get(self, request):
        member = get_member_admin_detail(request)
        app_config = AppConfig.objects.get(app_config_key='point_ratio')
        redeem_cash = member.member_point / int(app_config.app_config_value)
        response = {
            'member_id': member.member_id,
            'member_name': member.member_name,
            'member_phone': member.member_phone,
            'member_point': member.member_point,
            'redeem_cash': redeem_cash
        }
        return Response(response)


class AdminRegisterView(APIView):
    def post(self, request):
        # create user
        user_serializer = UserSerializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()

        # create admin
        user_id = user_serializer.data['id']
        admin_serializer = AdminSerializer(data=request.data)
        admin_serializer.is_valid(raise_exception=True)
        admin_serializer.save(user_id=user_id)
        return Response({'detail': 'Admin Created Successfully'}, status=status.HTTP_201_CREATED)


class AdminInfoView(APIView):

    @is_authentication(allowed_role=['ADMIN'])
    def get(self, request):
        admin = get_member_admin_detail(request)
        response = {
            'admin_id': admin.admin_id,
            'admin_name': admin.admin_name
        }
        return Response(response)
