from abc import ABC, abstractmethod

from django.db.models import Model
from django.db.models.signals import pre_save


class BaseUpdateSlugSignal(ABC):
    """
    The base class for changing the slug of a model
    object when a save method is called.
    """
    _sender = None
    _field_to_slugify = None

    def __init__(self):
        self.connect()

    @property
    def sender(self) -> Model:
        return self._sender

    @sender.setter
    @abstractmethod
    def sender(self, value):
        self.sender = value

    @property
    def field_to_slugify(self) -> str:
        return self._field_to_slugify

    @field_to_slugify.setter
    @abstractmethod
    def field_to_slugify(self, value):
        self._field_to_slugify = value

    def connect(self) -> None:
        pre_save.connect(self._handler, sender=self.sender)

    def _handler(self, sender, instance, *args, **kwargs) -> None:
        """
        Changes the slug if the object has just been created or
        if the field associated with the slug field has changed.
        """
        if not instance.id:
            instance.change_slug(self.field_to_slugify, commit=False)
        else:
            old_slugify_field = getattr(sender.objects.get(id=instance.id), self.field_to_slugify)
            new_slugify_field = getattr(instance, self.field_to_slugify)

            if old_slugify_field != new_slugify_field:
                instance.change_slug(self.field_to_slugify, commit=False)
