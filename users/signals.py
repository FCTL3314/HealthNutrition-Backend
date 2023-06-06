from django.db.models.signals import pre_save
from django.dispatch import receiver

from users.models import User


@receiver(pre_save, sender=User)
def change_slug(sender, instance, **kwargs):
    if not instance.id:
        instance.update_slug(commit=False)
    else:
        old_username = sender.objects.get(id=instance.id).username
        new_username = instance.username

        if old_username != new_username:
            instance.update_slug(commit=False)
