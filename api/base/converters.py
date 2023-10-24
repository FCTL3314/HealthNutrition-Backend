from typing import Protocol, TypeVar

from django.db.models import Model

T = TypeVar("T")
M_I = TypeVar("M_I", bound=Model)


class IDjangoORMToDTOConverter(Protocol[T]):
    def to_dto(self, django_model_instance: M_I) -> T:
        ...
