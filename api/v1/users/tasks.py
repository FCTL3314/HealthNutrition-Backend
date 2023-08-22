from celery import shared_task

from api.utils.mail import convert_html_to_email_message
from api.v1.users.models import EmailVerification


@shared_task
def send_verification_email(object_id: int) -> None:
    verification = EmailVerification.objects.get(id=object_id)
    verification.send_verification_email(
        subject_template_name="email/verification_email_subject.html",
        html_email_template_name="email/verification_email.html",
    )


@shared_task
def send_email(
    subject_template_name: str,
    email_template_name: str,
    to_email: list,
    context: dict | None = None,
) -> None:
    msg = convert_html_to_email_message(
        subject_template_name, email_template_name, [to_email], context
    )
    msg.send()
