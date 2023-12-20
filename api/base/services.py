from abc import abstractmethod
from typing import Protocol

from cacheops import CacheMiss, cache
from django.db.models import Model

from api.utils.errors import (
    ATTRIBUTE_MUST_BE_OVERRIDDEN,
    ATTRIBUTE_OR_METHOD_MUST_BE_OVERRIDDEN,
)


class IService(Protocol):
    """
    An interface for creating domain and infrastructure services.

    Response style:
        Instead of directly returning a Response class object from
        the execute method,it is recommended to create separate
        response methods, naming them according to this pattern:
        <response_name>_response.
        Example:
            def execute(self) -> APIResponse:
                if some_condition:
                    return self._successful_response()
                else:
                    return self._error_response()

            def _successful_response(self) -> APIResponse:
                return APIResponse(...)

            def _error_response(self) -> APIResponse:
                return APIResponse(...)
    """

    def execute(self):
        ...


class AbstractConditionalIncreaseService(IService):
    """
    Increases the field of an object by "increase_by"
    attribute when "_should_be_increased" condition
    is met.
    """

    field: str | None = None

    def __init__(
        self,
        instance: Model,
        increase_by: int = 1,
    ):
        assert self.field is not None, ATTRIBUTE_MUST_BE_OVERRIDDEN.format(
            attribute_name="field", class_name=self.__class__.__name__
        )
        self._instance = instance
        self._increase_by = increase_by

    def execute(self) -> None:
        if self._should_be_increased():
            self._increase()
            self._after_field_increased()

    @abstractmethod
    def _should_be_increased(self) -> bool:
        ...

    def _increase(self) -> None:
        """
        Increments the field of the model object by
        the value of the increase_by attribute.
        """
        current_value = getattr(self._instance, self.field)
        setattr(
            self._instance,
            self.field,
            current_value + self._increase_by,
        )
        self._instance.save()

    def _after_field_increased(self) -> None:
        """
        Logic after increasing the value of the object
        field.
        """
        ...


class BaseViewsIncreaseService(AbstractConditionalIncreaseService):
    """
    Increases the view counter of the model instance if
    the user has not yet viewed the object, that is, if
    the cache about its viewing is not in the database.
    """

    field = "views"
    view_cache_time: int | None = None
    view_cache_key: str | None = None

    def __init__(
        self,
        instance: Model,
        user_ip_address: str,
        increase_by: int = 1,
    ):
        super().__init__(instance, increase_by)
        assert self.view_cache_time is not None, ATTRIBUTE_MUST_BE_OVERRIDDEN.format(
            attribute_name="view_cache_time", class_name=self.__class__.__name__
        )
        self._user_ip_address = user_ip_address
        self._key = self.get_view_cache_key()

    def get_view_cache_key(self) -> str:
        """
        Returns the cache used to store the user's
        unique view.
        """
        assert (
            self.view_cache_key is not None
        ), ATTRIBUTE_OR_METHOD_MUST_BE_OVERRIDDEN.format(
            class_name=self.__class__.__name__,
            attribute_name="view_cache_key",
            method_name=self.get_view_cache_key.__name__,
        )
        return self.view_cache_key

    def _should_be_increased(self) -> bool:
        """
        Returns True if the user has not yet viewed this
        object, that is, if there is no saved cache about
        viewing it, otherwise False.
        """
        try:
            cache.get(self._key)
            return False
        except CacheMiss:
            return True

    def _after_field_increased(self) -> None:
        """
        Saves the user's view to the cache.
        """
        cache.set(self._key, True, self.view_cache_time)
