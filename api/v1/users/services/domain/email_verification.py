from datetime import datetime
from enum import Enum

from api.base.services import ServiceProto
from api.base.time_providers import TimeProviderProto, UTCTimeProvider
from api.v1.users.constants import EV_SENDING_INTERVAL_TIMEDELTA
from api.v1.users.services.schemas import EmailVerification, User


class EVAvailabilityStatus(Enum):
    """
    The status of the ability to send a verification email.
    """

    CAN_BE_SENT = 1
    SENDING_LIMIT_REACHED = 2
    ALREADY_VERIFIED = 3


class EVAvailabilityService(ServiceProto):
    """
    Calculates whether a verification email can be sent
    to the provided user.
    """

    def __init__(
        self,
        user: User,
        sending_interval_checker: ServiceProto,
    ):
        self._user = user
        self._sending_interval_checker = sending_interval_checker

    def execute(self) -> EVAvailabilityStatus:
        if self._user.is_verified:
            return EVAvailabilityStatus.ALREADY_VERIFIED
        if not self._sending_interval_checker.execute():
            return EVAvailabilityStatus.SENDING_LIMIT_REACHED
        return EVAvailabilityStatus.CAN_BE_SENT


class EVNextSendingTimeService(ServiceProto):
    """
    Calculates the date and time when the verification
    email can be resent.
    """

    def __init__(
        self,
        latest_verification: EmailVerification | None,
        time_provider: TimeProviderProto = UTCTimeProvider(),
    ):
        self._latest_verification = latest_verification
        self._time_provider = time_provider

    def execute(self) -> datetime:
        if self._latest_verification is None:
            return self._time_provider.now()
        return self._latest_verification.created_at + EV_SENDING_INTERVAL_TIMEDELTA


class EVSendingIntervalCheckerService(ServiceProto):
    """
    Calculates whether the allowed interval for sending
    the next verification email has passed.
    """

    def __init__(
        self,
        next_sending_time_calculator: ServiceProto,
        time_provider: TimeProviderProto = UTCTimeProvider(),
    ):
        self._next_sending_time_calculator = next_sending_time_calculator
        self._time_provider = time_provider

    def execute(self) -> bool:
        next_sending_datetime = self._next_sending_time_calculator.execute()
        return self._time_provider.now() >= next_sending_datetime
