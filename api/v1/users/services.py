from datetime import timedelta, datetime
from functools import wraps

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from api.v1.users.serializers import EmailVerificationSerializer, UserModelSerializer
from users.models import EmailVerification
from users.tasks import send_verification_email


class BaseEmailVerificationService:
    """
    A base service for email verification.
    """

    def __init__(self, user, request):
        self._user = user
        self._request = request

    @staticmethod
    def _request_user_matching_or_404(func):
        """
        Validate that the user is matching request user,
        otherwise raises a 404 error.
        """

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if self._user.is_request_user_matching(self._request):
                return func(self, *args, **kwargs)
            raise Http404

        return wrapper

    @staticmethod
    def _user_not_verified_or_400(func):
        """
        Validate that the user is not verified, otherwise
        raises a 400 error.
        """

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if not self._user.is_verified:
                return func(self, *args, **kwargs)
            return Response(
                {"detail": "Your email is already verified."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return wrapper


class EmailVerificationSender(BaseEmailVerificationService):
    serializer = EmailVerificationSerializer

    def __init__(self, user, request):
        super().__init__(user, request)
        self.domain = get_current_site(request).domain

    @staticmethod
    def _get_next_available_sending_datetime() -> datetime:
        latest_verification = EmailVerification.objects.latest("created_at")
        sending_interval = timedelta(seconds=settings.EMAIL_SENDING_SECONDS_INTERVAL)
        return latest_verification.created_at + sending_interval

    @BaseEmailVerificationService._request_user_matching_or_404
    @BaseEmailVerificationService._user_not_verified_or_400
    def send(self) -> Response:
        """
        Sends a verification email to the user if verification
        sending interval is passed.
        """
        if not self._user.is_verification_sending_interval_passed():
            response = {
                "detail": "Sending limit reached.",
                "retry_after": self._get_next_available_sending_datetime(),
            }
            return Response(response, status=status.HTTP_429_TOO_MANY_REQUESTS)
        verification = self._user.create_email_verification()
        send_verification_email.delay(object_id=verification.id, host=self.domain)
        serializer = self.serializer(verification)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserEmailVerifier(BaseEmailVerificationService):
    serializer = UserModelSerializer

    def __init__(self, user, request, code):
        super().__init__(user, request)
        self._verification = get_object_or_404(EmailVerification, user=user, code=code)

    @BaseEmailVerificationService._request_user_matching_or_404
    @BaseEmailVerificationService._user_not_verified_or_400
    def verify(self) -> Response:
        """
        Makes the users email verified if verification is not expired.
        """
        if self._verification.is_expired():
            return Response(
                {"detail": "The verification link has expired."},
                status=status.HTTP_410_GONE,
            )
        self._user.verify()
        serializer = self.serializer(self._user)
        return Response(serializer.data, status=status.HTTP_200_OK)
