from django import forms
from django.core.validators import EmailValidator

email_validator = EmailValidator("One or more email addresses are not valid. Please correct them.")


class EmailListField(forms.CharField):
    def to_python(self, value):
        if not value:
            return []
        return [email.strip() for email in value.split(",")]

    def validate(self, value):
        super().validate(value)
        for email in value:
            email_validator(email)
