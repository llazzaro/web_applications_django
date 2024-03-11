from datetime import datetime, timedelta
from functools import wraps

import jwt
from accounts.models import APIToken
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.http import HttpResponseForbidden


def generate_token(user: AbstractUser):
    """
    Generate a token for the user.
    """
    token, _ = APIToken.objects.get_or_create(user=user)
    return str(token.token)


def issue_jwt_token(user: AbstractUser) -> str:
    payload = {
        "id": user.id,
        "exp": datetime.utcnow() + timedelta(days=1),
    }

    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm="HS256")

    return token


def require_permission(permission_name: str):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            if not request.user.has_perm(permission_name):
                return HttpResponseForbidden()
            return func(request, *args, **kwargs)

        return wrapper

    return decorator
