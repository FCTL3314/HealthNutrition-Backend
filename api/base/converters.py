from typing import Protocol, TypeVar

from django.db.models import Model

T = TypeVar("T")
D_M = TypeVar("D_M", bound=Model)


class DjangoORMToDTOConverterProto(Protocol[T]):
    def to_dto(self, django_model_instance: D_M) -> T:
        ...
