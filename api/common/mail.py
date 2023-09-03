from django.conf import settings
from django.core.mail import send_mail as django_send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def convert_mail_subject(subject) -> str:
    return f"{subject} | Store Tracker"


def send_mail(
    subject: str,
    raw_message: str,
    context: dict | None = None,
    **kwargs,
) -> None:
    message = render_to_string(raw_message, context)

    django_send_mail(
        subject=convert_mail_subject(subject),
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        **kwargs,
    )


def send_html_mail(
    subject: str,
    html_email_template_name: str,
    context: dict | None = None,
    **kwargs,
) -> None:
    html_message = render_to_string(html_email_template_name, context)
    message = strip_tags(html_message)

    django_send_mail(
        subject=convert_mail_subject(subject),
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        html_message=html_message,
        **kwargs,
    )
