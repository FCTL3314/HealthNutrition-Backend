from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from api.common.models import ViewsModelMixin
from api.v1.products.managers import ProductManager, ProductTypeManager


class Product(ViewsModelMixin, models.Model):
    name = models.CharField(max_length=128, unique=True)
    price = models.FloatField()
    card_description = models.CharField(max_length=128)
    description = models.TextField()
    image = models.ImageField(upload_to="products/products")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    store = models.ForeignKey(to="stores.Store", on_delete=models.CASCADE)
    product_type = models.ForeignKey(
        to="products.ProductType", on_delete=models.CASCADE
    )
    views = models.PositiveIntegerField(default=0)
    slug = models.SlugField(unique=True)

    objects = ProductManager()

    def __str__(self):
        return f"{self.name} | {self.store}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse("api:v1:products:products-detail", args=(self.slug,))


class ProductType(ViewsModelMixin, models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=128)
    image = models.ImageField(upload_to="products/product_types")
    views = models.PositiveIntegerField(default=0)
    slug = models.SlugField(unique=True)

    objects = ProductTypeManager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse("api:v1:products:product-types-detail", args=(self.slug,))
