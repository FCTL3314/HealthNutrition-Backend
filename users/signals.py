from django.db.models.signals import pre_save
from django.dispatch import receiver

from users.models import User


@receiver(pre_save, sender=User)
def generate_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.update_slug()
    else:
        old_username = sender.objects.get(id=instance.id).username
        new_username = instance.username

        if old_username != new_username:
            instance.update_slug()
