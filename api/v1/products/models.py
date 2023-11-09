from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from api.common.models.mixins import ViewsModelMixin


class Product(ViewsModelMixin, models.Model):
    image = models.ImageField(upload_to="products")
    name = models.CharField(max_length=128, unique=True)
    short_description = models.CharField(max_length=128)
    nutrition = models.OneToOneField(to="nutrition.Nutrition", on_delete=models.CASCADE)
    category = models.ForeignKey(to="categories.Category", on_delete=models.CASCADE)
    comments = GenericRelation("comments.Comment")
    views = models.PositiveIntegerField(default=0)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse("api:v1:products:products-detail", args=(self.slug,))
