from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


def send_order_confirmation_email(order):

    subject = f"Booking Confirmation #{order.order_number}"

    context = {
        'order': order,
    }

    text_body = render_to_string(
        'checkout/emails/order_confirmation.txt',
        context
    )

    html_body = render_to_string(
        'checkout/emails/order_confirmation.html',
        context
    )

    email = EmailMultiAlternatives(
        subject,
        text_body,
        settings.DEFAULT_FROM_EMAIL,
        [order.email]
    )

    email.attach_alternative(html_body, "text/html")

    email.send()