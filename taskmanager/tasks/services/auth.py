from accounts.models import APIToken
from django.contrib.auth.models import AbstractUser


def generate_token(user: AbstractUser):
    """
    Generate a token for the user.
    """
    token, _ = APIToken.objects.get_or_create(user=user)
    return str(token.token)
