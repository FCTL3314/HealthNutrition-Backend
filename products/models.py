from django.conf import settings
from django.db import models
from django.db.models import Avg, Count, Max, Min

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

    average_price = models.FloatField(editable=False)
    highest_price = models.FloatField(editable=False)
    lowest_price = models.FloatField(editable=False)
    unique_store_count = models.IntegerField(editable=False)

    objects = ProductTypeManager()

    def __str__(self):
        return self.name

    def increment_views(self):
        self.views += 1
        self.save()

    def update_aggregates(self):
        aggregates = self.product_set.aggregate(Avg('price'), Max('price'), Min('price'), Count('store', distinct=True))

        self.average_price = aggregates['price__avg']
        self.highest_price = aggregates['price__max']
        self.lowest_price = aggregates['price__min']
        self.unique_store_count = aggregates['store__count']

        self.save()

    def get_rounded_average_price(self, digits=settings.PRICE_ROUNDING):
        return round(self.average_price, digits)

    def get_rounded_highest_price(self, digits=settings.PRICE_ROUNDING):
        return round(self.highest_price, digits)

    def get_rounded_lowest_price(self, digits=settings.PRICE_ROUNDING):
        return round(self.lowest_price, digits)
