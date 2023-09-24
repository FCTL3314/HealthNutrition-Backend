from abc import ABC, abstractmethod

from cacheops import CacheMiss, cache
from django.db.models import Model


class ViewsIncreaseService(ABC):
    field = "views"

    def __init__(
        self,
        instance: Model,
    ):
        assert hasattr(
            instance, self.field
        ), f"The provided instance doest not have a '{self.field}' field."
        self._instance = instance

    def increase(self, *args, **kwargs) -> None:
        current_value = getattr(self._instance, self.field)
        setattr(
            self._instance,
            self.field,
            current_value + 1,
        )
        self._instance.save()


class CachedViewsIncreaseService(ViewsIncreaseService):
    def __init__(
        self,
        instance: Model,
        address: str,
    ):
        super().__init__(instance)
        self._address = address

    def increase(self, *args, **kwargs) -> None:
        key = self.get_cache_key()
        try:
            cache.get(key)
        except CacheMiss:
            cache.set(key, True)
            super().increase(*args, **kwargs)

    @abstractmethod
    def get_cache_key(self) -> str:
        ...
