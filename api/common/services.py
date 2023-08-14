from abc import ABC, abstractmethod


class AbstractService(ABC):
    @abstractmethod
    def execute(self, *args, **kwargs):
        ...
