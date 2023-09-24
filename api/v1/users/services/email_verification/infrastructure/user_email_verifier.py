from dataclasses import dataclass

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.serializers import Serializer

from api.common.services.base import IService
from api.responses import APIResponse
from api.utils.errors import ErrorMessage
from api.v1.users.models import EmailVerification

User = get_user_model()


@dataclass
class UserVerificationErrors:
    VERIFICATION_EXPIRED = ErrorMessage(
        "The verification code has expired.", "verification_code_expired"
    )
    INVALID_CODE = ErrorMessage(
        "Invalid verification code.", "invalid_verification_code"
    )


class UserEmailVerifierService(IService):
    """
    Verify the provided user's email, if possible,
    otherwise returns an error response.
    """

    def __init__(
        self,
        email_verification_serializer: type[Serializer],
        user_serializer: type[Serializer],
        user: User,
        data: dict,
    ):
        email_verification_serializer(data=data).is_valid(raise_exception=True)
        self._user_serializer = user_serializer
        self._user = user
        self._code = data["code"]
        self._email_verification = EmailVerification.objects.filter(
            user=self._user,
            code=self._code,
        ).first()

    def execute(self) -> APIResponse:
        if self._email_verification is None:
            return self._invalid_verification_code_response()
        if self._email_verification.is_expired:
            return self._verification_expired_response()
        self._user.verify()
        return self._successfully_verified_response()

    def _successfully_verified_response(self) -> APIResponse:
        return APIResponse(
            self._user_serializer(self._user).data,
            status=status.HTTP_200_OK,
        )

    @staticmethod
    def _invalid_verification_code_response() -> APIResponse:
        return APIResponse(
            detail=UserVerificationErrors.INVALID_CODE.message,
            code=UserVerificationErrors.INVALID_CODE.code,
            status=status.HTTP_400_BAD_REQUEST,
        )

    @staticmethod
    def _verification_expired_response() -> APIResponse:
        return APIResponse(
            detail=UserVerificationErrors.VERIFICATION_EXPIRED.message,
            code=UserVerificationErrors.VERIFICATION_EXPIRED.code,
            status=status.HTTP_410_GONE,
        )
