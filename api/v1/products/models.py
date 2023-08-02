from django.db import models
from django.urls import reverse

from api.v1.products.managers import ProductManager, ProductTypeManager


class Product(models.Model):
    name = models.CharField(max_length=128)
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

    def get_absolute_url(self) -> str:
        return reverse("products:product-detail", args=(self.slug,))


class ProductType(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=128)
    image = models.ImageField(upload_to="products/product_types")
    views = models.PositiveIntegerField(default=0)
    slug = models.SlugField(unique=True)

    objects = ProductTypeManager()

    def __str__(self):
        return self.name
