from celery import shared_task
from django.conf import settings

from users.models import EmailVerification


@shared_task
def send_verification_email(object_id):
    verification = EmailVerification.objects.get(id=object_id)
    verification.send_verification_email(
        subject='Special Recipe | Email Verification',
        html_email_template_name='users/email/email_verification_content.html',
        protocol=settings.PROTOCOL,
    )
