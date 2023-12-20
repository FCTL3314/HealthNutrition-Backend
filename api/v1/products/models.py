from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.postgres.indexes import GinIndex
from django.db import models
from django.urls import reverse

from api.common.models.mixins import ViewsModelMixin, AutoSlugModelMixin
from api.v1.products.managers import ProductManager


class Product(AutoSlugModelMixin, ViewsModelMixin, models.Model):
    image = models.ImageField(upload_to="products")
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=128)
    nutrition = models.OneToOneField(
        to="nutrition.Nutrition",
        related_name="product",
        on_delete=models.PROTECT,
    )
    category = models.ForeignKey(
        to="categories.Category", null=True, on_delete=models.SET_NULL
    )
    comments = GenericRelation("comments.Comment")
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ProductManager()

    SLUG_RELATED_FIELD = "name"

    class Meta:
        indexes = (GinIndex(fields=("name", "short_description")),)

    def __str__(self):
        return self.name

    def get_absolute_url(self) -> str:
        return reverse("api:v1:products:products-detail", args=(self.slug,))
