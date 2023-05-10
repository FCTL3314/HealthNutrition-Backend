from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from users.models import User


@receiver(pre_save, sender=User)
def generate_slug(sender, instance, **kwargs):
    if not instance.id:
        instance.slug = slugify(instance.username)

    old_username = sender.objects.get(id=instance.id).username
    new_username = instance.username

    if old_username != new_username:
        instance.slug = slugify(instance.username)
