import uuid

import jwt
from accounts.models import APIToken
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpRequest
from ninja.security import HttpBearer


class APITokenAuth(HttpBearer):
    def authenticate(self, request: HttpRequest, token: str) -> str | None:
        try:
            uuid.UUID(token, version=4)
        except ValueError:
            return None

        if APIToken.objects.filter(token=token).exists():
            request.user = APIToken.objects.get(token=token).user
            return token
        else:
            return None


class JWTAuth(HttpBearer):
    def authenticate(self, request: HttpRequest, token: str) -> str | None:
        try:
            # Decode the JWT token
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])

            user = get_user_model().objects.get(id=payload["id"])
            request.user = user
            return user, token
        except Exception as e:
            return None
