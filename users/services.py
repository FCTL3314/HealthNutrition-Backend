from django.conf import settings
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import get_object_or_404

from users.models import EmailVerification
from users.tasks import send_verification_email


def send_email_verification(user, request):
    """Sends an email verification message to the user's email."""
    seconds_since_last_sending = user.seconds_since_last_email_verification_sending()

    if user.is_verified:
        messages.warning(request, "You have already verified your email.")
    elif seconds_since_last_sending < settings.EMAIL_SEND_INTERVAL_SECONDS:
        seconds_left = settings.EMAIL_SEND_INTERVAL_SECONDS - seconds_since_last_sending
        messages.warning(request, f"Please wait {seconds_left} to resend the confirmation email.")
    else:
        verification = user.create_email_verification()
        current_site = get_current_site(request)
        send_verification_email.delay(object_id=verification.id, host=current_site.domain)


def handle_email_verification(user, code, request):
    """
    Handles the email verification process for the user and verify their email
    when all conditions are met.
    """
    verification = get_object_or_404(EmailVerification, user=user, code=code)

    if user.is_verified:
        messages.warning(request, "Your email has already been verified.")
    elif verification.is_expired():
        messages.warning(request, "The verification link has expired.")
    else:
        user.verify()
