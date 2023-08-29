from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from django.db.models import Model

from api.utils.errors import ATTRIBUTE_UNDEFINED_TEMPLATE

DTOType = TypeVar("DTOType")


class IORMToDTOAdapter(ABC, Generic[DTOType]):
    @classmethod
    @abstractmethod
    def to_dto(cls, model_instance: Model) -> DTOType:
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
    def fields(self) -> tuple[str, ...] | list[str]:
        raise AttributeError(
            ATTRIBUTE_UNDEFINED_TEMPLATE.format(
                class_name=self.__class__.__name__,
                attribute_name="fields",
            ),
        )

    def get_model_instance_kwargs(self, model_instance: Model) -> dict:
        return {field: getattr(model_instance, field) for field in self.fields}

    def to_dto(self, model_instance: Model) -> DTOType:
        return self.dto_class(**self.get_model_instance_kwargs(model_instance))
