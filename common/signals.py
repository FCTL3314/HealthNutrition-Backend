from abc import ABC, abstractmethod

from django.db.models.signals import pre_save

from common.models import change_slug


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
        pre_save.connect(self.handler, sender=self.sender)

    def handler(self, sender, instance, *args, **kwargs):
        slugify_field = self.slugify_field
        slugify_string = getattr(instance, slugify_field)

        if not instance.id:
            change_slug(instance=instance, slugify_string=slugify_string, commit=False)
        else:
            old_slugify_field = getattr(sender.objects.get(id=instance.id), slugify_field)
            new_slugify_field = getattr(instance, slugify_field)

            if old_slugify_field != new_slugify_field:
                change_slug(instance=instance, slugify_string=slugify_string, commit=False)
