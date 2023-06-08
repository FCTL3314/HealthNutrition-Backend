from abc import ABC, abstractmethod

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
    def sender(self):
        pass

    @property
    @abstractmethod
    def slugify_field(self):
        pass

    def connect(self):
        pre_save.connect(self._handler, sender=self.sender)

    def _handler(self, sender, instance, *args, **kwargs):
        if not instance.id:
            instance.change_slug(self.slugify_field, commit=False)
        else:
            old_slugify_field = getattr(sender.objects.get(id=instance.id), self.slugify_field)
            new_slugify_field = getattr(instance, self.slugify_field)

            if old_slugify_field != new_slugify_field:
                instance.change_slug(self.slugify_field, commit=False)
