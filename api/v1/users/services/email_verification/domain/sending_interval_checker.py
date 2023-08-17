from api.common.services import AbstractService
from api.common.time_providers import AbstractTimeProvider, UTCTimeProvider
from api.v1.users.services.data_transfer import EmailVerificationDTO


class EVSendingIntervalCheckerService(AbstractService):
    """
    Calculates whether the allowed interval for sending
    the next verification email has passed.
    """

    def __init__(
        self,
        latest_verification: EmailVerificationDTO | None,
        next_sending_time_calculator: AbstractService,
        time_provider: AbstractTimeProvider = UTCTimeProvider(),
    ):
        self._latest_verification = latest_verification
        self._next_sending_time_calculator = next_sending_time_calculator
        self._time_provider = time_provider

    def execute(self) -> bool:
        if self._latest_verification is None:
            return True
        next_sending_datetime = self._next_sending_time_calculator.execute()
        return self._time_provider.now > next_sending_datetime
