from datetime import datetime
from enum import Enum

from api.base.time_providers import ITimeProvider, UTCTimeProvider
from api.utils.time import round_datetime
from api.v1.users.constants import EV_SENDING_INTERVAL_TIMEDELTA
from api.v1.users.services.schemas import EmailVerification, User


class EVAvailabilityStatus(Enum):
    """
    The status of the ability to send a verification email.
    """

    CAN_BE_SENT = 1
    SENDING_LIMIT_REACHED = 2
    ALREADY_VERIFIED = 3


def get_ev_sending_availability_status(
    user: User,
    latest_verification: EmailVerification | None,
) -> EVAvailabilityStatus:
    """
    Calculates whether a verification email can be sent
    to the provided user.
    """
    if user.is_verified:
        return EVAvailabilityStatus.ALREADY_VERIFIED
    if not is_ev_sending_interval_passed(latest_verification):
        return EVAvailabilityStatus.SENDING_LIMIT_REACHED
    return EVAvailabilityStatus.CAN_BE_SENT


def is_ev_sending_interval_passed(
    latest_verification: EmailVerification | None,
    time_provider: ITimeProvider = UTCTimeProvider(),
) -> bool:
    """
    Calculates whether the allowed interval for sending
    the next verification email has passed.
    """
    rounded_now = round_datetime(time_provider.now())
    rounded_ev_next_sending_datetime = round_datetime(
        get_ev_next_sending_datetime(latest_verification)
    )

    return rounded_now >= rounded_ev_next_sending_datetime


def get_ev_next_sending_datetime(
    latest_verification: EmailVerification | None,
    time_provider: ITimeProvider = UTCTimeProvider(),
) -> datetime:
    """
    Calculates the date and time when the verification
    email can be resent.
    """
    if latest_verification is None:
        return time_provider.now()
    return latest_verification.created_at + EV_SENDING_INTERVAL_TIMEDELTA
