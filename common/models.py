from django.utils.text import slugify


def change_slug(instance, slugify_field, commit=True):
    slugify_string = getattr(instance, slugify_field)
    instance.slug = slugify(slugify_string)
    if commit:
        instance.save(update_fields=('slug',))
