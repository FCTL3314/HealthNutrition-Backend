from django.contrib.postgres.indexes import GinIndex
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from api.common.models.mixins import ViewsModelMixin
from api.v1.categories.managers import CategoryManager


class Category(ViewsModelMixin, models.Model):
    image = models.ImageField(upload_to="categories")
    name = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=128)
    views = models.PositiveIntegerField(default=0)
    slug = models.SlugField(unique=True)

    objects = CategoryManager()

    class Meta:
        verbose_name_plural = "categories"
        indexes = (GinIndex(fields=("name", "description")),)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse("api:v1:categories:categories-detail", args=(self.slug,))
