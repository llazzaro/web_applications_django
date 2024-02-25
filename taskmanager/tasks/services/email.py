from django.core.mail import send_mail


def send_contact_email(subject: str, message: str, from_email: str, to_email: str) -> None:
    send_mail(subject, message, from_email, [to_email])
