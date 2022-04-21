import jwt
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
            admin = Admin.objects.get(user_id=payload['id'])
            return admin
        except Exception as e:
            raise NotFound(e)
