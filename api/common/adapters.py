from abc import ABC, abstractmethod
from typing import Any, Generic, Iterable, TypeVar

from django.db.models import Model

from api.utils.errors import ATTRIBUTE_UNDEFINED_TEMPLATE

DTOType = TypeVar("DTOType")


class IORMToDTOAdapter(ABC, Generic[DTOType]):
    @abstractmethod
    def to_dto(self, model_instance: Model) -> DTOType:
        ...


class BaseORMToDTOAdapter(IORMToDTOAdapter[DTOType]):
    @property
    def dto_class(self) -> type[DTOType]:
        raise AttributeError(
            ATTRIBUTE_UNDEFINED_TEMPLATE.format(
                class_name=self.__class__.__name__,
                attribute_name="dto_class",
            ),
        )

    @property
    def fields(self) -> Iterable[str]:
        raise AttributeError(
            ATTRIBUTE_UNDEFINED_TEMPLATE.format(
                class_name=self.__class__.__name__,
                attribute_name="fields",
            ),
        )

    def get_instance_kwargs(self, instance: Model) -> dict[str, Any]:
        return {field: getattr(instance, field) for field in self.fields}

    def to_dto(self, instance: Model) -> DTOType:
        return self.dto_class(**self.get_instance_kwargs(instance))
