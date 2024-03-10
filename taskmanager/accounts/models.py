import uuid

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, User
from django.db import models


class APIToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return str(self.token)


# class Organization(models.Model):
#     name = models.CharField(max_length=255)
#
#
# class CustomUserManager(BaseUserManager):
#     def create_user(self, username, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError("The Email field must be set")
#         email = self.normalize_email(email)
#         user = self.model(username=username, email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self.db)
#
#         return user
#
#     def create_superuser(self, username, email, password=None, **extra_fields):
#         extra_fields.setdefault("is_staff", True)
#         extra_fields.setdefault("is_superuser", True)
#
#         if extra_fields.get("is_staff") is not True:
#             raise ValueError("Superuser must have is_staff=True.")
#         if extra_fields.get("is_superuser") is not True:
#             raise ValueError("Superuser must have is_superuser=True.")
#
#         extra_fields.setdefault("organization_id", 1)
#
#         return self.create_user(username, email, password, **extra_fields)
#
# class TaskManagerUser(AbstractUser):
#     organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
#     username = models.CharField(max_length=150, unique=True)
#     email = models.EmailField(unique=True)
#     objects = CustomUserManager()
#
#     class Meta:
#         unique_together = (
#             ("organization", "username"),
#             ("organization", "email"),
#         )
#
# class UserProfile(models.Model):
#     user = models.OneToOneField(TaskManagerUser, on_delete=models.CASCADE)
#     biography = models.TextField(max_length=500, blank=True)
#     photo = models.ImageField(upload_to="user_photos/")
#
#     def __str__(self):
#         return self.user.username
