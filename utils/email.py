# utils/email.py

from django.core.mail import send_mail
from django.conf import settings

def send_contact_email(subject: str, message: str) -> None:
    """
    Sends an email to CONTACT_FORM_RECEIVER if both required settings are defined.
    """
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', None)
    recipient = getattr(settings, 'CONTACT_FORM_RECEIVER', None)

    if not from_email or not recipient:
        # Skip sending if either email is missing
        return

    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=[recipient],
    )
