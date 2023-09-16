from abc import ABC, abstractmethod


class IService(ABC):
    @abstractmethod
    def execute(self, *args, **kwargs):
        ...
