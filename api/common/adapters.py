from abc import ABC, abstractmethod
from typing import Callable, Generic, TypeVar

from django.db.models import Model

DTOType = TypeVar("DTOType")


class AbstractORMToDTOAdapter(ABC, Generic[DTOType]):
    @classmethod
    @abstractmethod
    def to_dto(cls, model_instance: Model) -> DTOType:
        ...


class BaseORMToDTOAdapter(AbstractORMToDTOAdapter[DTOType]):
    dto_class: Callable
    fields: tuple[str, ...] | list[str]

    @classmethod
    def get_model_instance_kwargs(cls, model_instance: Model) -> dict:
        return {field: getattr(model_instance, field) for field in cls.fields}

    @classmethod
    def to_dto(cls, model_instance: Model) -> DTOType:
        return cls.dto_class(**cls.get_model_instance_kwargs(model_instance))
