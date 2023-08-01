from abc import ABC
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from api.v1.users.models import EmailVerification
from api.v1.users.serializers import (CurrentUserSerializer,
                                      EmailVerificationSerializer)
from api.v1.users.tasks import send_verification_email


class AbstractEmailVerificationService(ABC):
    def __init__(self, user, request):
        self._user = user
        self._request = request
        if not self._user.is_request_user_matching(request):
            raise Http404


class BaseEmailVerificationSenderService(AbstractEmailVerificationService):
    """
    A base service for sending a verification email to the users.
    """

    def __init__(self, user, request):
        super().__init__(user, request)
        self.domain = get_current_site(request).domain

    def send(self):
        if self._user.is_verification_sending_interval_passed():
            verification = self._user.create_email_verification()
            send_verification_email.delay(object_id=verification.id, domain=self.domain)
            return self.successfully_sent(verification)
        return self.sending_interval_not_passed()

    def successfully_sent(self, verification):
        pass

    def sending_interval_not_passed(self):
        pass


class BaseEmailVerifierService(AbstractEmailVerificationService):
    """
    A base service for verifying users email.
    """

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
    serializer = EmailVerificationSerializer

    def successfully_sent(self, verification: EmailVerification) -> Response:
        serializer = self.serializer(verification)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def _get_next_available_sending_datetime() -> datetime:
        latest_verification = EmailVerification.objects.latest("created_at")
        sending_interval = timedelta(seconds=settings.EMAIL_SENDING_SECONDS_INTERVAL)
        return latest_verification.created_at + sending_interval

    def sending_interval_not_passed(self) -> Response:
        response = {
            "detail": "Sending limit reached.",
            "retry_after": self._get_next_available_sending_datetime(),
        }
        return Response(response, status=status.HTTP_429_TOO_MANY_REQUESTS)


class UserEmailVerifier(BaseEmailVerifierService):
    serializer = CurrentUserSerializer

    def successfully_verified(self) -> Response:
        serializer = self.serializer(self._user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def verification_expired(self) -> Response:
        return Response(
            {"detail": "The verification link has expired."},
            status=status.HTTP_410_GONE,
        )

    def email_already_verified(self) -> Response:
        return Response(
            {"detail": "Your email is already verified."},
            status=status.HTTP_400_BAD_REQUEST,
        )
