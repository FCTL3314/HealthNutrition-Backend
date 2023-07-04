from functools import wraps

from django.conf import settings
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import get_object_or_404

from users.models import EmailVerification
from users.tasks import send_verification_email


class BaseEmailVerificationService:
    """
    A base service for email verification.
    """

    def __init__(self, request):
        self._user = request.user
        self._request = request

    @staticmethod
    def _validate_user_not_verified(func):
        """
        Validate that the user is not verified, otherwise
        creates an error message.
        """

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if not self._user.is_verified:
                return func(self, *args, **kwargs)
            else:
                messages.warning(self._request, "You have already verified your email.")

        return wrapper


class EmailVerificationSender(BaseEmailVerificationService):
    def __init__(self, request):
        super().__init__(request)
        self.domain = get_current_site(request).domain

    @BaseEmailVerificationService._validate_user_not_verified
    def send(self) -> None:
        """
        Sends a verification email to the user if verification
        sending interval is passed.
        """
        if self._user.is_verification_sending_interval_passed():
            verification = self._user.create_email_verification()
            send_verification_email.delay(object_id=verification.id, host=self.domain)
        else:
            seconds_since_last_sending = (
                self._user.seconds_since_last_email_verification_sending()
            )
            seconds_left = (
                    settings.EMAIL_SENDING_SECONDS_INTERVAL - seconds_since_last_sending
            )
            messages.warning(
                self._request,
                f"Please wait {seconds_left} seconds to resend the verification email.",
            )


class UserEmailVerifier(BaseEmailVerificationService):
    def __init__(self, request, code):
        super().__init__(request)
        self._verification = get_object_or_404(
            EmailVerification, user=self._user, code=code
        )

    @BaseEmailVerificationService._validate_user_not_verified
    def verify(self) -> None:
        """
        Makes the users email verified if verification is not
        expired.
        """

        if self._verification.is_expired():
            messages.warning(self._request, "The verification link has expired.")
        else:
            self._user.verify()
