from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string


def send_contact_email(subject: str, message: str) -> None:
    """
    Sends an email to CONTACT_FORM_RECEIVER if both required settings are defined.
    """
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', None)
    recipient = getattr(settings, 'CONTACT_FORM_RECEIVER', None)
    email_enabled = getattr(settings, "EMAIL_ENABLED", False)
    
    if not email_enabled:
        # Skip sending if either email is missing
        return

    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=[recipient],
    )


def send_order_confirmation_email(order) -> None:
    """
    Sends different HTML emails to the admin and the customer with order details.
    """
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', None)
    admin_email = getattr(settings, 'CONTACT_FORM_RECEIVER', None)
    customer_email = order.email

    email_enabled = getattr(settings, "EMAIL_ENABLED", False)

    if not email_enabled:
        return

    # Send to admin
    if admin_email:
        subject_admin = f"New Order Placed - {order.first_name} {order.last_name}"
        text_content_admin = f"New order from {order.first_name} {order.last_name}, total £{order.total}"
        html_content_admin = render_to_string("emails/order_confirmation_admin.html", {"order": order})

        msg_admin = EmailMultiAlternatives(
            subject=subject_admin,
            body=text_content_admin,
            from_email=from_email,
            to=[admin_email],
        )
        msg_admin.attach_alternative(html_content_admin, "text/html")
        msg_admin.send()

    # Send to customer
    if customer_email:
        subject_customer = "Thank you for your order!"
        text_content_customer = f"Thanks {order.first_name}, your order has been placed. Total: £{order.total}"
        html_content_customer = render_to_string("emails/order_confirmation_customer.html", {"order": order})

        msg_customer = EmailMultiAlternatives(
            subject=subject_customer,
            body=text_content_customer,
            from_email=from_email,
            to=[customer_email],
        )
        msg_customer.attach_alternative(html_content_customer, "text/html")
        msg_customer.send()