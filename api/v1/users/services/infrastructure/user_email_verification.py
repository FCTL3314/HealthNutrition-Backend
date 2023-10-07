from functools import cached_property

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.serializers import Serializer

from api.base.services import ServiceProto
from api.common.tasks import send_html_mail
from api.responses import APIResponse
from api.utils.errors import ErrorMessage
from api.v1.users.models import EmailVerification
from api.v1.users.services.converters import EVConverter
from api.v1.users.services.domain.email_verification import (
    EVAvailabilityStatus,
    get_ev_next_sending_datetime,
    get_ev_sending_availability_status,
)
from api.v1.users.services.schemas import EmailVerification as EmailVerificationSchema

User = get_user_model()


class EVSendErrors:
    SENDING_LIMIT_REACHED = ErrorMessage(
        "Sending limit reached.", "sending_limit_reached"
    )
    ALREADY_VERIFIED = ErrorMessage(
        "Your email is already verified.", "email_already_verified"
    )


class UserVerificationErrors:
    VERIFICATION_EXPIRED = ErrorMessage(
        "The verification code has expired.", "verification_code_expired"
    )
    INVALID_CODE = ErrorMessage(
        "Invalid verification code.", "invalid_verification_code"
    )


class EVSenderService(ServiceProto):
    """
    Sends a verification email to the provided user, if possible,
    otherwise returns an error response.
    """

    def __init__(
        self,
        serializer_class: type[Serializer],
        user: User,
    ):
        self._serializer_class = serializer_class
        self._user = user

    @cached_property
    def _latest_verification_schema(self) -> EmailVerificationSchema | None:
        latest_verification = EmailVerification.objects.last_sent(self._user.id)
        if latest_verification is None:
            return None
        return EVConverter().to_dto(latest_verification)

    def execute(self) -> APIResponse:
        availability_status = get_ev_sending_availability_status(
            self._user, self._latest_verification_schema
        )
        return self._handle_availability_status(availability_status)

    def _handle_availability_status(
        self, availability_status: EVAvailabilityStatus
    ) -> APIResponse:
        """
        Based on the status of the ability to send an email,
        either sends it or returns an error message.
        """
        match availability_status:
            case EVAvailabilityStatus.CAN_BE_SENT:
                return self._email_sent_response(self._send())
            case EVAvailabilityStatus.SENDING_LIMIT_REACHED:
                return self._sending_limit_reached_response()
            case EVAvailabilityStatus.ALREADY_VERIFIED:
                return self._already_verified_response()

    def _send(self) -> EmailVerification:
        """
        Creates an EmailVerification object and sends it.
        """
        email_verification = EmailVerification.objects.create(user=self._user)
        send_html_mail.delay(
            subject="Your email verification",
            html_email_template_name="email/verification_email.html",
            recipient_list=[email_verification.user.email],
            context={
                "username": email_verification.user.username,
                "verification_code": email_verification.code,
            },
        )
        return email_verification

    def _email_sent_response(
        self, email_verification: EmailVerification
    ) -> APIResponse:
        return APIResponse(
            self._serializer_class(email_verification).data,
            status=status.HTTP_201_CREATED,
        )

    def _sending_limit_reached_response(self) -> APIResponse:
        return APIResponse(
            detail=EVSendErrors.SENDING_LIMIT_REACHED.message,
            code=EVSendErrors.SENDING_LIMIT_REACHED.code,
            messages={
                "retry_after": get_ev_next_sending_datetime(
                    self._latest_verification_schema
                ),
            },
            status=status.HTTP_429_TOO_MANY_REQUESTS,
        )

    @staticmethod
    def _already_verified_response() -> APIResponse:
        return APIResponse(
            detail=EVSendErrors.ALREADY_VERIFIED.message,
            code=EVSendErrors.ALREADY_VERIFIED.code,
            status=status.HTTP_400_BAD_REQUEST,
        )


class UserEmailVerifierService(ServiceProto):
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
