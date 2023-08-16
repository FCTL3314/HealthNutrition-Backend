from enum import Enum

from api.common.services import AbstractService


class EVAvailabilityStatus(Enum):
    CAN_BE_SENT = 1
    SENDING_LIMIT_REACHED = 2


class EVAvailabilityService(AbstractService):
    def __init__(
        self,
        sending_interval_checker: AbstractService,
    ):
        self._sending_interval_checker = sending_interval_checker

    def execute(self) -> EVAvailabilityStatus:
        if self._sending_interval_checker.execute():
            return EVAvailabilityStatus.CAN_BE_SENT
        return EVAvailabilityStatus.SENDING_LIMIT_REACHED
