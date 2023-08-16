from datetime import datetime, timedelta

from api.common.services import AbstractService
from api.v1.users.constants import EMAIL_SENDING_SECONDS_INTERVAL
from api.v1.users.services.data_transfer import EmailVerificationDTO


class EVNextSendingTimeService(AbstractService):
    def execute(self, latest_verification: EmailVerificationDTO) -> datetime:
        return self._calculate_next_sending_datetime(latest_verification)

    @staticmethod
    def _calculate_next_sending_datetime(
        latest_verification: EmailVerificationDTO,
    ) -> datetime:
        sending_interval = timedelta(seconds=EMAIL_SENDING_SECONDS_INTERVAL)
        return latest_verification.created_at + sending_interval
