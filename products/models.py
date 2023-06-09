from django.conf import settings
from django.db import models
from django.urls import reverse

from common.models import IncrementMixin, SlugifyMixin
from products.managers import ProductManager, ProductTypeManager
from utils.cache import get_cached_data_or_set_new


class Product(SlugifyMixin, IncrementMixin, models.Model):
    name = models.CharField(max_length=128)
    price = models.FloatField()
    card_description = models.CharField(max_length=128)
    description = models.TextField()
    image = models.ImageField(upload_to='products/products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    store = models.ForeignKey(to='stores.Store', on_delete=models.CASCADE)
    product_type = models.ForeignKey(to='products.ProductType', on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0)
    slug = models.SlugField(unique=True)

    objects = ProductManager()

    def __str__(self):
        return f'{self.name} | {self.store}'

    def get_absolute_url(self):
        return reverse('products:product-detail', args=(self.slug,))

    def get_comments(self):
        return self.productcomment_set.order_by('-created_at')


class ProductType(SlugifyMixin, IncrementMixin, models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=128)
    image = models.ImageField(upload_to='products/product_types')
    views = models.PositiveIntegerField(default=0)
    slug = models.SlugField(unique=True)

    objects = ProductTypeManager()

    def __str__(self):
        return self.name

    def get_products_with_stores(self):
        callback = self.product_set.prefetch_related('store').all
        return get_cached_data_or_set_new(
            key=settings.PRODUCTS_CACHE_TEMPLATE.format(id=self.id),
            callback=callback,
            timeout=settings.PRODUCTS_CACHE_TIME,
        )
