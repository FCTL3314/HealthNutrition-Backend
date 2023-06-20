from abc import ABC, abstractmethod

from django.db.models import Model
from django.db.models.signals import pre_save


class BaseUpdateSlugSignal(ABC):
    """
    The base class for changing the slug of a model
    object when a save method is called.
    """

    def __init__(self):
        self.connect()

    @property
    @abstractmethod
    def sender(self) -> Model:
        pass

    @property
    @abstractmethod
    def slug_related_field(self) -> str:
        pass

    def connect(self) -> None:
        pre_save.connect(self._handler, sender=self.sender)

    def _handler(self, sender, instance, *args, **kwargs) -> None:
        """
        Changes the slug if the object has just been created or
        if the field associated with the slug field has changed.
        """
        if kwargs["raw"]:
            return
        if not instance.id:
            instance.change_slug(self.slug_related_field, commit=False)
        else:
            old_slugify_field = getattr(
                sender.objects.get(id=instance.id), self.slug_related_field
            )
            new_slugify_field = getattr(instance, self.slug_related_field)

            if old_slugify_field != new_slugify_field:
                instance.change_slug(self.slug_related_field, commit=False)
