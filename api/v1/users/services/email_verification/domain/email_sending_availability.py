from enum import Enum

from api.common.services.base import IService
from api.v1.users.services.data_transfer import UserDTO


class EVAvailabilityStatus(Enum):
    """
    The status of the ability to send a verification email.
    """

    CAN_BE_SENT = 1
    SENDING_LIMIT_REACHED = 2
    ALREADY_VERIFIED = 3


class EVAvailabilityService(IService):
    """
    Calculates whether a verification email can be sent
    to the provided user.
    """

    def __init__(
        self,
        user: UserDTO,
        sending_interval_checker: IService,
    ):
        self._user = user
        self._sending_interval_checker = sending_interval_checker

    def execute(self) -> EVAvailabilityStatus:
        if self._user.is_verified:
            return EVAvailabilityStatus.ALREADY_VERIFIED
        if not self._sending_interval_checker.execute():
            return EVAvailabilityStatus.SENDING_LIMIT_REACHED
        return EVAvailabilityStatus.CAN_BE_SENT
