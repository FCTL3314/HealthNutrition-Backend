from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from api.v1.users.models import EmailVerification
from api.v1.users.serializers import CurrentUserSerializer, UserVerificationSerializer


class UserEmailVerifierService:
    serializer_class = CurrentUserSerializer

    def __init__(self, user, data):
        UserVerificationSerializer(data=data).is_valid(raise_exception=True)
        self._user = user
        self._code = data["code"]

    def verify(self) -> Response:
        verification = get_object_or_404(
            EmailVerification, user=self._user, code=self._code
        )
        if not verification.is_expired():
            if not self._user.is_verified:
                self._user.verify()
                return self.successfully_verified()
            return self.email_already_verified_response()
        return self.verification_expired_response()

    def successfully_verified(self) -> Response:
        serializer = self.serializer_class(self._user)
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
