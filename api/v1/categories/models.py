from django.contrib.postgres.indexes import GinIndex
from django.db import models
from django.urls import reverse

from api.common.models.mixins import ViewsModelMixin, AutoSlugModelMixin
from api.v1.categories.managers import CategoryManager


class Category(AutoSlugModelMixin, ViewsModelMixin, models.Model):
    image = models.ImageField(upload_to="categories")
    name = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=128)
    views = models.PositiveIntegerField(default=0)

    objects = CategoryManager()

    SLUG_RELATED_FIELD = "name"

    class Meta:
        verbose_name_plural = "categories"
        indexes = (GinIndex(fields=("name", "description")),)

    def __str__(self):
        return self.name

    def get_absolute_url(self) -> str:
        return reverse("api:v1:categories:categories-detail", args=(self.slug,))
