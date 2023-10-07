from datetime import datetime, timezone
from typing import Protocol, TypeVar

T = TypeVar("T")


class TimeProviderProto(Protocol[T]):
    """
    Provides a protocol for obtaining an
    infrastructure-agnostic time.
    """

    def now(self) -> T:
        ...


class UTCTimeProvider(TimeProviderProto[datetime]):
    def now(self) -> datetime:
        return datetime.now(tz=timezone.utc)
