from celery import shared_task
from django.conf import settings

from users.models import EmailVerification, User
from utils.mail import convert_html_to_email_message


@shared_task
def send_verification_email(object_id):
    verification = EmailVerification.objects.get(id=object_id)
    verification.send_verification_email(
        subject_template_name='users/email/email_verification_subject.html',
        html_email_template_name='users/email/email_verification_content.html',
        protocol=settings.PROTOCOL,
    )


@shared_task
def send_password_reset_email(subject_template_name, email_template_name, to_email, context=None):
    context['user'] = User.objects.get(id=context['user'])

    msg = convert_html_to_email_message(subject_template_name, email_template_name, [to_email], context)
    msg.send()
