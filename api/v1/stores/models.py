from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from api.common.models.mixins import ViewsModelMixin
from api.v1.comments.models import Comment


class Store(ViewsModelMixin, models.Model):
    name = models.CharField(max_length=64, unique=True)
    url = models.URLField(unique=True)
    logo = models.ImageField(upload_to="stores")
    description = models.TextField()
    views = models.PositiveIntegerField(default=0)
    slug = models.SlugField(unique=True)
    comments = GenericRelation(Comment)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse("api:v1:stores:stores-detail", args=(self.slug,))
