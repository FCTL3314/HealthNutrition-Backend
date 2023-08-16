from datetime import datetime, timedelta

from api.common.services import AbstractService
from api.common.time_providers import AbstractTimeProvider, UTCTimeProvider
from api.v1.users.constants import EMAIL_SENDING_SECONDS_INTERVAL
from api.v1.users.services.data_transfer import EmailVerificationDTO


class EVNextSendingTimeService(AbstractService):
    def __init__(
        self,
        latest_verification: EmailVerificationDTO | None,
        time_provider: AbstractTimeProvider = UTCTimeProvider(),
    ):
        self._latest_verification = latest_verification
        self._time_provider = time_provider

    def execute(self) -> datetime:
        return self._calculate_next_sending_datetime()

    def _calculate_next_sending_datetime(self) -> datetime:
        sending_interval = timedelta(seconds=EMAIL_SENDING_SECONDS_INTERVAL)
        if self._latest_verification is None:
            return self._time_provider.now
        return self._latest_verification.created_at + sending_interval
