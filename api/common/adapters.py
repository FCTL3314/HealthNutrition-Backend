from abc import ABC, abstractmethod

from django.db.models import Model


class AbstractModelToDTOAdapter(ABC):
    @staticmethod
    @abstractmethod
    def to_dto(model_instance: Model):
        ...
