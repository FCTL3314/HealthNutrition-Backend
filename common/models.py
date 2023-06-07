from django.utils.text import slugify


def change_slug(instance, slugify_string, commit=True):
    instance.slug = slugify(slugify_string)
    if commit:
        instance.save(update_fields=('slug',))
