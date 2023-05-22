from django.db import models

from products.managers import ProductTypeManager


class Product(models.Model):
    name = models.CharField(max_length=128)
    price = models.FloatField()
    card_description = models.CharField(max_length=128)
    description = models.TextField()
    image = models.ImageField(upload_to='products/products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    store = models.ForeignKey(to='stores.Store', on_delete=models.CASCADE)
    product_type = models.ForeignKey(to='products.ProductType', on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return f'{self.name} | {self.store}'


class ProductType(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=128)
    image = models.ImageField(upload_to='products/product_types')
    views = models.PositiveIntegerField(default=0)
    slug = models.SlugField(unique=True)

    objects = ProductTypeManager()

    def __str__(self):
        return self.name

    def increment_views(self):
        self.views += 1
        self.save(update_fields=('views',))
