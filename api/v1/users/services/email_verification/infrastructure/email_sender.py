from dataclasses import dataclass
from functools import cached_property

from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from api.common.services import AbstractService
from api.v1.users.models import EmailVerification
from api.v1.users.services.data_transfer import EmailVerificationDTO, EVAdapter
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
class EVSendMessages:
    SENDING_LIMIT_REACHED = "Sending limit reached."


class EVSenderService(AbstractService):
    def __init__(self, serializer_class: type[Serializer], user_id: int):
        self._serializer_class = serializer_class
        self._user_id = user_id
        self._latest_verification = EmailVerification.objects.last_sent(user_id)
        self._next_sending_time_calculator = EVNextSendingTimeService(
            self.latest_verification_dto
        )
        sending_interval_checker = EVSendingIntervalCheckerService(
            self.latest_verification_dto,
            self._next_sending_time_calculator,
        )
        self._sending_availability_service = EVAvailabilityService(
            sending_interval_checker,
        )

    @cached_property
    def latest_verification_dto(self) -> EmailVerificationDTO | None:
        if self._latest_verification is None:
            return None
        return EVAdapter.to_dto(self._latest_verification)

    def execute(self) -> Response:
        availability_status = self._sending_availability_service.execute()
        return self._handle_availability_status(availability_status)

    def _handle_availability_status(
        self, availability_status: EVAvailabilityStatus
    ) -> Response:
        match availability_status:
            case EVAvailabilityStatus.CAN_BE_SENT:
                return self._email_sent_response(self._send())
            case EVAvailabilityStatus.SENDING_LIMIT_REACHED:
                return self._sending_limit_reached_response()

    def _send(self) -> EmailVerification:
        email_verification = EmailVerification.objects.create(user_id=self._user_id)
        send_verification_email.delay(object_id=email_verification.id)
        return email_verification

    def _email_sent_response(self, email_verification: EmailVerification) -> Response:
        return Response(
            self._serializer_class(email_verification).data,
            status=status.HTTP_201_CREATED,
        )

    def _sending_limit_reached_response(self) -> Response:
        data = {
            "detail": EVSendMessages.SENDING_LIMIT_REACHED,
            "retry_after": self._next_sending_time_calculator.execute(),
        }
        return Response(data, status=status.HTTP_429_TOO_MANY_REQUESTS)
