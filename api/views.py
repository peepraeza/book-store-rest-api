import datetime
import jwt

from .models import User, Admin

from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.exceptions import AuthenticationFailed, NotFound
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Book, Member
from api.serializers import BookSerializer, UserSerializer
from .models import Member
from .serializers import MemberSerializer


# Create your views here.


@csrf_exempt
def bookApi(request, book_id=0):
    validateAuthentication(request, ['ADMIN'])
    if request.method == 'GET':
        books = Book.objects.all()
        books_serializer = BookSerializer(books, many=True)
        return JsonResponse(books_serializer.data, safe=False)
    elif request.method == 'POST':
        book_data = JSONParser().parse(request)
        books_serializer = BookSerializer(data=book_data)
        if books_serializer.is_valid():
            books_serializer.save()
            return JsonResponse("Added Successfully", safe=False)
        return JsonResponse("Failed to Add", safe=False)
    elif request.method == 'PUT':
        book_data = JSONParser().parse(request)
        book = Book.objects.get(book_id=book_data['book_id'])
        book_serializer = BookSerializer(book, data=book_data)
        if book_serializer.is_valid():
            book_serializer.save()
            return JsonResponse("Updated Successfully", safe=False)
        return JsonResponse("Failed to Update")
    elif request.method == 'DELETE':
        book = Book.objects.get(book_id=book_id)
        book.delete()
        return JsonResponse("Deleted Successfully", safe=False)


def validateAuthentication(request, role):
    token = request.headers['Authorization']
    if not token:
        raise AuthenticationFailed('Unauthenticated!')

    try:
        payload = jwt.decode(token, 'secret', algorithm=['HS256'])
    except:
        print('error Authen')
        raise AuthenticationFailed('Unauthenticated!')

    user = User.objects.filter(id=payload['id']).first()

    if 'ADMIN' in role:
        admin = Admin.objects.filter(user_id=user.id).first()
        if admin is None:
            raise NotFound('pee')
    elif 'MEMBER' in role:
        member = Member.objects.filter(user_id=user.id).first()
        if member is None:
            raise AuthenticationFailed('Unauthenticated!')
    else:
        raise AuthenticationFailed('Unauthenticated!')


# Create your views here.
class RegisterView(APIView):
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


class LoginView(APIView):
    def post(self, request):
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
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return response


class UserView(APIView):

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


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response
