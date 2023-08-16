from datetime import datetime, timezone

from api.common.services import AbstractService
from api.v1.users.constants import EMAIL_SENDING_SECONDS_INTERVAL
from api.v1.users.services.data_transfer import EmailVerificationDTO


class EVSendingIntervalCheckerService(AbstractService):
    def execute(self, latest_verification: EmailVerificationDTO):
        return self._is_sending_interval_passed(latest_verification)

    @staticmethod
    def _is_sending_interval_passed(latest_verification: EmailVerificationDTO) -> bool:
        if latest_verification is None:
            return False
        elapsed_time = datetime.now(tz=timezone.utc) - latest_verification.created_at
        return elapsed_time.seconds > EMAIL_SENDING_SECONDS_INTERVAL
