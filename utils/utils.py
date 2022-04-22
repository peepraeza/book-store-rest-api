import jwt
from rest_framework.exceptions import NotFound

from appconfig.models import AppConfig
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
