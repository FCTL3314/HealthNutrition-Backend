from datetime import datetime, timezone
from typing import Protocol


class TimeProviderProto(Protocol):
    def now(self) -> datetime:
        ...


class UTCTimeProvider(TimeProviderProto):
    def now(self) -> datetime:
        return datetime.now(tz=timezone.utc)
