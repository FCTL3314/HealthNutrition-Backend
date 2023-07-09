from celery import shared_task

from users.models import EmailVerification
from utils.mail import convert_html_to_email_message


@shared_task
def send_verification_email(object_id, domain):
    verification = EmailVerification.objects.get(id=object_id)
    verification.send_verification_email(
        subject_template_name="users/email/email_verification_subject.html",
        html_email_template_name="users/email/email_verification_content.html",
        domain=domain,
    )


@shared_task
def send_email(subject_template_name, email_template_name, to_email, context=None):
    msg = convert_html_to_email_message(
        subject_template_name, email_template_name, [to_email], context
    )
    msg.send()
