from datetime import datetime, timedelta

from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from api.v1.users.models import EmailVerification
from api.v1.users.serializers import (
    EmailVerificationSerializer,
    CurrentUserSerializer,
    VerifyUserSerializer,
)
from api.v1.users.tasks import send_verification_email


class EmailVerificationSenderService:
    serializer_class = EmailVerificationSerializer

    def __init__(self, request):
        self.user = request.user

    def send(self) -> Response:
        if self.user.is_verification_sending_interval_passed():
            verification = self.user.create_email_verification()
            send_verification_email.delay(object_id=verification.id)
            serializer = self.serializer_class(verification)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return self._sending_limit_reached_response()

    def _sending_limit_reached_response(self) -> Response:
        response = {
            "detail": "Sending limit reached.",
            "retry_after": self._get_next_available_sending_datetime(),
        }
        return Response(response, status=status.HTTP_429_TOO_MANY_REQUESTS)

    @staticmethod
    def _get_next_available_sending_datetime() -> datetime:
        latest_verification = EmailVerification.objects.latest("created_at")
        sending_interval = timedelta(seconds=settings.EMAIL_SENDING_SECONDS_INTERVAL)
        return latest_verification.created_at + sending_interval


class UserEmailVerifierService:
    serializer_class = CurrentUserSerializer

    def __init__(self, request):
        VerifyUserSerializer(data=request.data).is_valid(raise_exception=True)
        self.user = request.user
        self._code = request.data["code"]

    def verify(self) -> Response:
        verification = get_object_or_404(
            EmailVerification, user=self.user, code=self._code
        )
        if not verification.is_expired():
            if not self.user.is_verified:
                self.user.verify()
                return self.successfully_verified()
            return self.email_already_verified_response()
        return self.verification_expired_response()

    def successfully_verified(self) -> Response:
        serializer = self.serializer_class(self.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def verification_expired_response() -> Response:
        return Response(
            {"detail": "The verification link has expired."},
            status=status.HTTP_410_GONE,
        )

    @staticmethod
    def email_already_verified_response() -> Response:
        return Response(
            {"detail": "Your email is already verified."},
            status=status.HTTP_400_BAD_REQUEST,
        )
