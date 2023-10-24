from datetime import datetime, timezone
from typing import Protocol, TypeVar

T = TypeVar("T")


class ITimeProvider(Protocol[T]):
    """
    Provides an interface for obtaining an
    infrastructure-agnostic time.
    """

    def now(self) -> T:
        ...


class UTCTimeProvider(ITimeProvider[datetime]):
    def now(self) -> datetime:
        return datetime.now(tz=timezone.utc)
