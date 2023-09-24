from abc import ABC, abstractmethod

from django.db.models import Model
from rest_framework.serializers import Serializer


class IService(ABC):
    @abstractmethod
    def execute(self, *args, **kwargs):
        ...


class IRetrieveService(ABC):
    def __init__(self, instance: Model, serializer: type[Serializer]):
        self._instance = instance
        self._serializer = serializer

    @abstractmethod
    def retrieve(self, *args, **kwargs):
        ...
