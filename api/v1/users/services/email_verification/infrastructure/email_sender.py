from dataclasses import dataclass
from functools import cached_property

from rest_framework import status
from rest_framework.serializers import Serializer

from api.common.services import AbstractService
from api.responses import APIResponse
from api.utils.errors import ErrorMessage
from api.v1.users.models import EmailVerification, User
from api.v1.users.services.data_transfer import (
    EmailVerificationDTO,
    EVAdapter,
    UserAdapter,
)
from api.v1.users.services.email_verification.domain.email_sending_availability import (
    EVAvailabilityService,
    EVAvailabilityStatus,
)
from api.v1.users.services.email_verification.domain.next_sending_time_calculator import (
    EVNextSendingTimeService,
)
from api.v1.users.services.email_verification.domain.sending_interval_checker import (
    EVSendingIntervalCheckerService,
)
from api.v1.users.tasks import send_verification_email


@dataclass
class EVSendErrors:
    SENDING_LIMIT_REACHED = ErrorMessage(
        "Sending limit reached.", "sending_limit_reached."
    )
    ALREADY_VERIFIED = ErrorMessage(
        "Your email is already verified.", "email_already_verified."
    )


class EVSenderService(AbstractService):
    """
    Sends a confirmation email to the provided user, if possible,
    otherwise returns an error message.
    """

    def __init__(
        self,
        serializer_class: type[Serializer],
        user: User,
    ):
        self._serializer_class = serializer_class
        self._user = user
        self._next_sending_time_calculator = EVNextSendingTimeService(
            self.latest_verification_dto
        )
        self._sending_availability_service = EVAvailabilityService(
            UserAdapter.to_dto(user),
            EVSendingIntervalCheckerService(
                self.latest_verification_dto,
                self._next_sending_time_calculator,
            ),
        )

    @cached_property
    def latest_verification_dto(self) -> EmailVerificationDTO | None:
        latest_verification = EmailVerification.objects.last_sent(self._user.id)
        if latest_verification is None:
            return None
        return EVAdapter.to_dto(latest_verification)

    def execute(self) -> APIResponse:
        availability_status = self._sending_availability_service.execute()
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
        email_verification = EmailVerification.objects.create(user_id=self._user.id)
        send_verification_email.delay(object_id=email_verification.id)
        return email_verification

    def _email_sent_response(
        self, email_verification: EmailVerification
    ) -> APIResponse:
        return APIResponse(
            self._serializer_class(email_verification).data,
            status=status.HTTP_201_CREATED,
        )

    def _sending_limit_reached_response(self) -> APIResponse:
        messages = {
            "retry_after": self._next_sending_time_calculator.execute(),
        }
        return APIResponse(
            detail=EVSendErrors.SENDING_LIMIT_REACHED.message,
            code=EVSendErrors.SENDING_LIMIT_REACHED.code,
            messages=messages,
            status=status.HTTP_429_TOO_MANY_REQUESTS,
        )

    @staticmethod
    def _already_verified_response():
        return APIResponse(
            detail=EVSendErrors.ALREADY_VERIFIED.message,
            code=EVSendErrors.ALREADY_VERIFIED.code,
            status=status.HTTP_429_TOO_MANY_REQUESTS,
        )
