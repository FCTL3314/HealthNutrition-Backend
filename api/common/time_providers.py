from abc import ABC, abstractmethod
from datetime import datetime, timezone


class AbstractTimeProvider(ABC):
    @property
    @abstractmethod
    def now(self) -> datetime:
        ...


class BaseTimeProvider(AbstractTimeProvider):
    time_zone: timezone

    @property
    def now(self) -> datetime:
        return datetime.now(tz=self.time_zone)


class UTCTimeProvider(BaseTimeProvider):
    time_zone = timezone.utc
