from abc import ABC, abstractmethod
from typing import Protocol

from cacheops import CacheMiss, cache
from django.db.models import Model
from rest_framework.serializers import Serializer


class ServiceProto(Protocol):
    def execute(self):
        ...


class IRetrieveService(ABC):
    def __init__(self, instance: Model, serializer: type[Serializer]):
        self._instance = instance
        self._serializer = serializer

    @abstractmethod
    def retrieve(self, *args, **kwargs):
        ...


class ViewsIncreaseService(ServiceProto):
    """
    Increases the view counter of the model instance if
    the user has not yet viewed the object, that is, if
    the cache about its viewing is not in the database.
    """

    views_field = "views"

    def __init__(
        self,
        instance: Model,
        user_ip_address: str,
    ):
        assert hasattr(
            instance, self.views_field
        ), f"The provided instance doest not have a '{self.views_field}' field."
        self._instance = instance
        self._user_ip_address = user_ip_address
        self._key = self.get_cache_key()

    def execute(self) -> None:
        if not self._is_already_viewed:
            self._increase()
            self._save_user_view()

    def _increase(self) -> None:
        """
        Increases the views field of the model instance.
        """
        current_value = getattr(self._instance, self.views_field)
        setattr(
            self._instance,
            self.views_field,
            current_value + 1,
        )
        self._instance.save()

    @property
    def _is_already_viewed(self) -> bool:
        try:
            cache.get(self._key)
            return True
        except CacheMiss:
            return False

    def _save_user_view(self):
        """
        Saves the user's browsing to the cache.
        """
        cache.set(self._key, True)

    @abstractmethod
    def get_cache_key(self) -> str:
        """
        Returns the cache used to store the user's
        unique view.
        """
        ...
