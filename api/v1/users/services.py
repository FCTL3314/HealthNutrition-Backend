from datetime import timedelta
from functools import wraps

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from users.models import EmailVerification
from users.tasks import send_verification_email


class EmailVerificationService:

    def __init__(self, user, request):
        self.user = user
        self.request = request

    @staticmethod
    def _request_user_matching_or_404(func):

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if self.user.is_request_user_matching(self.request):
                return func(self, *args, **kwargs)
            raise Http404

        return wrapper

    @staticmethod
    def _user_not_verified_or_400(func):

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if not self.user.is_verified:
                return func(self, *args, **kwargs)
            return Response(
                {"detail": "Your email is already verified."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return wrapper

    @_request_user_matching_or_404
    @_user_not_verified_or_400
    def send_verification(self, serializer_class) -> Response:
        if not self.user.can_send_email_verification():
            last_verification = self.user.valid_email_verifications().first()
            interval = timedelta(seconds=settings.EMAIL_SENDING_SECONDS_INTERVAL)
            response = {
                "detail": "Sending limit reached.",
                "retry_after": last_verification.created_at + interval,
            }
            return Response(response, status=status.HTTP_429_TOO_MANY_REQUESTS)
        else:
            verification = self.user.create_email_verification()
            current_site = get_current_site(self.request)
            send_verification_email.delay(
                object_id=verification.id, host=current_site.domain
            )
            serializer = serializer_class(verification, partial=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    @_request_user_matching_or_404
    @_user_not_verified_or_400
    def verify_user(self, code) -> Response:
        verification = get_object_or_404(EmailVerification, user=self.user, code=code)
        if not verification.is_expired():
            self.user.verify()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {'detail': 'Verification link was expired.'},
                status=status.HTTP_410_GONE,
            )
