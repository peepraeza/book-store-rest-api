import jwt
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from rest_framework.exceptions import AuthenticationFailed


def is_authentication(allowed_role=[]):
    def decorator(func):
        def wrap(request, *args, **kwargs):
            req = list(args)[0]
            token = req.headers['Authorization']
            if not token:
                raise AuthenticationFailed('Unauthenticated!')

            try:
                payload = jwt.decode(token, 'secret', algorithm=['HS256'])
            except Exception as e:
                raise AuthenticationFailed(e)

            user = User.objects.filter(id=payload['id']).first()
            if user is None:
                raise AuthenticationFailed()
            role = payload['role']
            if role not in allowed_role:
                raise PermissionDenied('PermissionDenied')

            return func(request, *args, **kwargs)

        return wrap

    return decorator
