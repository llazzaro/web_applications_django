from datetime import datetime, timedelta

import jwt
from accounts.models import APIToken
from django.conf import settings
from django.contrib.auth.models import AbstractUser


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
