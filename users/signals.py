from abc import abstractmethod, ABC

from django.db.models import Model
from django.db.models.signals import pre_save
from django.dispatch import receiver

from users.models import User
from common.models import change_slug


class BaseUpdateSlugSignal:
    model: Model
    slugify_string: str

    @abstractmethod
    def get_slugify_string(self):
        pass

    @receiver(pre_save, sender=User)
    def handler(self, sender, instance, *args, **kwargs):
        if not instance.id:
            change_slug(instance=instance, slugify_string=instance.username, commit=False)
        else:
            old_username = sender.objects.get(id=instance.id).username
            new_username = instance.username

            if old_username != new_username:
                change_slug(instance=instance, slugify_string=instance.username, commit=False)


class UserUpdateSlugSignal(BaseUpdateSlugSignal):
    pass
