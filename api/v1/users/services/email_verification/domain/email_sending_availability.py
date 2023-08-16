from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from api.common.services import AbstractService
from api.v1.users.services.data_transfer import EmailVerificationDTO


class EVAvailabilityStatus(Enum):
    CAN_BE_SENT = 1
    SENDING_LIMIT_REACHED = 2


@dataclass
class EVAvailabilityResponse:
    status: EVAvailabilityStatus
    retry_after: datetime | None = None


class EVAvailabilityService(AbstractService):
    def __init__(
        self,
        latest_verification: EmailVerificationDTO,
        next_sending_time_calculator: AbstractService,
        sending_interval_checker: AbstractService,
    ):
        self._latest_verification = latest_verification
        self._next_sending_time_calculator = next_sending_time_calculator
        self._sending_interval_checker = sending_interval_checker

    def execute(self) -> EVAvailabilityResponse:
        if self._sending_interval_checker.execute(self._latest_verification):
            return self._can_be_sent_response()
        return self._sending_limit_reached_response()

    @staticmethod
    def _can_be_sent_response():
        return EVAvailabilityResponse(status=EVAvailabilityStatus.CAN_BE_SENT)

    def _sending_limit_reached_response(self):
        return EVAvailabilityResponse(
            status=EVAvailabilityStatus.SENDING_LIMIT_REACHED,
            retry_after=self._next_sending_time_calculator.execute(
                self._latest_verification
            ),
        )
