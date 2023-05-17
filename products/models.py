from django.db import models
from django.db.models import Avg, Count, Max, Min


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
    slug = models.SlugField(unique=True)

    average_price = models.FloatField(editable=False)
    highest_price = models.FloatField(editable=False)
    lowest_price = models.FloatField(editable=False)
    unique_store_count = models.IntegerField(editable=False)

    def __str__(self):
        return self.name

    def update_aggregates(self):
        aggregates = self.product_set.aggregate(Avg('price'), Max('price'), Min('price'), Count('store', distinct=True))

        self.average_price = aggregates['price__avg']
        self.highest_price = aggregates['price__max']
        self.lowest_price = aggregates['price__min']
        self.unique_store_count = aggregates['store__count']
        self.save()

    def get_rounded_average_price(self, digits=2):
        return round(self.average_price, digits)

    def get_rounded_highest_price(self, digits=2):
        return round(self.highest_price, digits)

    def get_rounded_lowest_price(self, digits=2):
        return round(self.lowest_price, digits)
