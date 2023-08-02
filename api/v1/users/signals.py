from api.v1.users.models import USER_SLUG_RELATED_FIELD


def update_slug_signal(sender, instance, *args, **kwargs) -> None:
    if not kwargs["raw"]:
        if not instance.id:
            instance.change_slug(commit=False)
        else:
            old_slugify_field = getattr(
                sender.objects.get(id=instance.id), USER_SLUG_RELATED_FIELD
            )
            new_slugify_field = getattr(instance, USER_SLUG_RELATED_FIELD)

            if old_slugify_field != new_slugify_field:
                instance.change_slug(commit=False)
