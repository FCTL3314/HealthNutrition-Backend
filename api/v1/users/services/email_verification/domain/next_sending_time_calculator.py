from datetime import datetime

from api.common.services import IService
from api.common.time_providers import AbstractTimeProvider, UTCTimeProvider
from api.v1.users.constants import EV_SENDING_INTERVAL_TIMEDELTA
from api.v1.users.services.data_transfer import EmailVerificationDTO


class EVNextSendingTimeService(IService):
    """
    Calculates the date and time when the verification
    email can be resent.
    """

    def __init__(
        self,
        latest_verification: EmailVerificationDTO | None,
        time_provider: AbstractTimeProvider = UTCTimeProvider(),
    ):
        self._latest_verification = latest_verification
        self._time_provider = time_provider

    def execute(self) -> datetime:
        if self._latest_verification is None:
            return self._time_provider.now
        return self._latest_verification.created_at + EV_SENDING_INTERVAL_TIMEDELTA
