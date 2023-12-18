from copy import copy

from django.db.models import Model
from django.utils.text import slugify
from unidecode import unidecode


def slugify_unique(value: str, model: type[Model], slug_field: str = "slug") -> str:
    original_slug = slugify(unidecode(value))
    new_slug = copy(original_slug)
    number = 1
    while model.objects.filter(**{slug_field: new_slug}).exists():
        new_slug = f"{original_slug}-{number}"
        number += 1
    return new_slug
