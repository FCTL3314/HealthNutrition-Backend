from api.common.services import IService
from api.common.time_providers import AbstractTimeProvider, UTCTimeProvider


class EVSendingIntervalCheckerService(IService):
    """
    Calculates whether the allowed interval for sending
    the next verification email has passed.
    """

    def __init__(
        self,
        next_sending_time_calculator: IService,
        time_provider: AbstractTimeProvider = UTCTimeProvider(),
    ):
        self._next_sending_time_calculator = next_sending_time_calculator
        self._time_provider = time_provider

    def execute(self) -> bool:
        next_sending_datetime = self._next_sending_time_calculator.execute()
        return self._time_provider.now >= next_sending_datetime
