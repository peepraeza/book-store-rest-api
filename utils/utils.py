import jwt
from django.http import JsonResponse
from rest_framework.exceptions import NotFound

from user.models import Member, Admin


def get_member_admin_detail(reqeust):
    token = reqeust.headers['Authorization']
    payload = jwt.decode(token, 'secret', algorithm=['HS256'])

    if payload['role'] == 'MEMBER':
        try:
            member = Member.objects.get(user_id=payload['id'])
            return member
        except Exception as e:
            raise NotFound(e)
    else:
        try:
            print('admin')
            admin = Admin.objects.get(user_id=payload['id'])
            print(admin)
            return admin
        except Exception as e:
            raise NotFound(e)


def error_404(request, exception):
    message = 'This endpoint is not found'
    response = JsonResponse(data={'detail': message, 'status_code': 404})
    response.status_code = 404
    return response


def error_500(request):
    message = 'An error occurred, its on us'
    response = JsonResponse(data={'detail': message, 'status_code': 500})
    response.status_code = 500
    return response
