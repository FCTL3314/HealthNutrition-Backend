from datetime import datetime, timedelta

from django.conf import settings
from rest_framework import status
from rest_framework.response import Response

from api.v1.users.serializers import EmailVerificationSerializer, CurrentUserSerializer
from users.models import EmailVerification
from users.services import BaseEmailVerificationSenderService, BaseEmailVerifierService


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
