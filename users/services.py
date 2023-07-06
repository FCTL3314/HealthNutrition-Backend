from abc import ABC

from django.conf import settings
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.http import Http404
from django.shortcuts import get_object_or_404

from users.models import EmailVerification
from users.tasks import send_verification_email


class AbstractEmailVerificationService(ABC):
    def __init__(self, user, request):
        self._user = user
        self._request = request
        if not self._user.is_request_user_matching(request):
            raise Http404


class BaseEmailVerificationSenderService(AbstractEmailVerificationService):
    def __init__(self, user, request):
        super().__init__(user, request)
        self.domain = get_current_site(request).domain

    def send(self):
        if self._user.is_verification_sending_interval_passed():
            verification = self._user.create_email_verification()
            send_verification_email.delay(object_id=verification.id, host=self.domain)
            return self.successfully_sent(verification)
        return self.sending_interval_not_passed()

    def successfully_sent(self, verification):
        pass

    def sending_interval_not_passed(self):
        pass


class BaseEmailVerifierService(AbstractEmailVerificationService):
    def __init__(self, user, request, code):
        super().__init__(user, request)
        self._verification = get_object_or_404(
            EmailVerification, user=self._user, code=code
        )

    def verify(self):
        if not self._verification.is_expired():
            if not self._user.is_verified:
                self._user.verify()
                return self.successfully_verified()
            return self.email_already_verified()
        return self.verification_expired()

    def successfully_verified(self):
        pass

    def verification_expired(self):
        pass

    def email_already_verified(self):
        pass


class EmailVerificationSender(BaseEmailVerificationSenderService):
    def sending_interval_not_passed(self) -> None:
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


class UserEmailVerifier(BaseEmailVerifierService):
    def verification_expired(self) -> None:
        messages.warning(self._request, "The verification link has expired.")

    def email_already_verified(self) -> None:
        messages.warning(self._request, "Your email has already been verified.")
