from celery import shared_task

from api.v1.users.models import EmailVerification
from utils.mail import convert_html_to_email_message


@shared_task
def send_verification_email(object_id):
    verification = EmailVerification.objects.get(id=object_id)
    verification.send_verification_email(
        subject_template_name="email/email_verification_subject.html",
        html_email_template_name="email/email_verification.html",
    )


@shared_task
def send_email(subject_template_name, email_template_name, to_email, context=None):
    msg = convert_html_to_email_message(
        subject_template_name, email_template_name, [to_email], context
    )
    msg.send()
