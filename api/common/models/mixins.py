from django.db import models

from api.utils.errors import (
    ATTRIBUTE_OR_METHOD_MUST_BE_OVERRIDDEN,
)
from api.utils.text import slugify_unique


class ViewsModelMixin(models.Model):
    views = models.PositiveIntegerField(default=0)

    class Meta:
        abstract = True


class SlugModelMixin(models.Model):
    SLUG_FIELD_KWARGS = {"unique": True}

    slug = models.SlugField(**SLUG_FIELD_KWARGS)

    class Meta:
        abstract = True


class AutoSlugModelMixin(SlugModelMixin):
    """
    Automatically creates a slug based on the slug
    related field when save method is called.
    """

    SLUG_RELATED_FIELD: str | None = None

    class Meta:
        abstract = True

    def save(self, *args, **kwargs) -> None:
        if not hasattr(self, self.get_slug_related_field()):
            raise ValueError(
                f"Slug related field of {self.__class__.__name__} class is not exists."
            )
        if not self.slug:
            related_text = getattr(self, self.get_slug_related_field())
            self.slug = slugify_unique(related_text, self.__class__)
        return super().save(*args, **kwargs)

    def get_slug_related_field(self) -> str:
        assert (
            self.SLUG_RELATED_FIELD is not None
        ), ATTRIBUTE_OR_METHOD_MUST_BE_OVERRIDDEN.format(
            class_name=self.__class__.__name__,
            attribute_name="SLUG_RELATED_FIELD",
            method_name=self.get_slug_related_field.__name__,
        )
        return self.SLUG_RELATED_FIELD
