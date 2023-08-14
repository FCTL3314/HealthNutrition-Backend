from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from django.utils.timezone import now
from rest_framework import status

from api.common.adapters import AbstractModelToDTOAdapter
from api.common.services import AbstractService
from api.v1.users.constants import EMAIL_SENDING_SECONDS_INTERVAL
from api.v1.users.models import EmailVerification
from api.v1.users.services import EmailVerificationDTO, UserDTO
from api.v1.users.services.email_verification.next_email_sending_time import (
    EVNextSendingTimeService,
)
from api.v1.users.tasks import send_verification_email


class EVSendingStatus(Enum):
    SUCCESSFULLY_SENT = ("Successfully sent.", 1)
    SENDING_LIMIT_REACHED = ("Sending limit reached.", 2)

    def __init__(self, message, value):
        self._message = message
        self._value = value

    @property
    def message(self):
        return self._message

    @property
    def value(self):
        return self._value


@dataclass
class EVSendingResponse:
    status: EVSendingStatus
    status_code: int
    data: EmailVerificationDTO | None = None
    retry_after: datetime | None = None


class EVSenderService(AbstractService):
    def __init__(
        self,
        next_sending_time_calculator: EVNextSendingTimeService,
        email_verification_adapter: AbstractModelToDTOAdapter,
    ):
        self._next_sending_time_calculator = next_sending_time_calculator
        self._email_verification_adapter = email_verification_adapter

    def execute(
        self, user: UserDTO, latest_verification: EmailVerificationDTO
    ) -> EVSendingResponse:
        if self._is_sending_interval_passed(latest_verification):
            verification = self._send(user)
            return self._successfully_sent_response(verification)
        return self._sending_limit_reached_response(latest_verification)

    @staticmethod
    def _is_sending_interval_passed(latest_verification: EmailVerificationDTO) -> bool:
        if latest_verification is None:
            return False
        elapsed_time = now() - latest_verification.created_at
        return elapsed_time.seconds > EMAIL_SENDING_SECONDS_INTERVAL

    def _send(self, user: UserDTO) -> EmailVerificationDTO:
        email_verification = self._email_verification_adapter.to_dto(
            EmailVerification.objects.create(user_id=user.id)
        )
        send_verification_email.delay(object_id=email_verification.id)
        return email_verification

    @staticmethod
    def _successfully_sent_response(verification: EmailVerificationDTO):
        return EVSendingResponse(
            status=EVSendingStatus.SUCCESSFULLY_SENT,
            status_code=status.HTTP_201_CREATED,
            data=verification,
        )

    def _sending_limit_reached_response(
        self, latest_verification: EmailVerificationDTO
    ):
        return EVSendingResponse(
            status=EVSendingStatus.SENDING_LIMIT_REACHED,
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            retry_after=self._next_sending_time_calculator.execute(latest_verification),
        )
