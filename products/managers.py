from django.conf import settings
from django.db import models
from django.db.models import Avg, Count, Max, Min, Q
from django.db.models.functions import Round

from utils.cache import get_cached_data_or_set_new


class ProductQuerySet(models.QuerySet):
    def price_aggregation(self):
        aggregations = self.aggregate(
            price__min=Round(Min("price"), settings.PRICE_ROUNDING),
            price__max=Round(Max("price"), settings.PRICE_ROUNDING),
            price__avg=Round(Avg("price"), settings.PRICE_ROUNDING),
        )
        return aggregations


class ProductManager(models.Manager):
    _queryset_class = ProductQuerySet

    def search(self, query):
        return self.filter(
            Q(name__icontains=query) | Q(card_description__icontains=query)
        )


class ProductTypeQuerySet(models.QuerySet):
    def product_price_annotation(self):
        return self.annotate(
            product__price__avg=Round(Avg("product__price"), settings.PRICE_ROUNDING),
            product__price__max=Round(Max("product__price"), settings.PRICE_ROUNDING),
            product__price__min=Round(Min("product__price"), settings.PRICE_ROUNDING),
            product__store__count=Count("product__store", distinct=True),
        )


class ProductTypeManager(models.Manager):
    _queryset_class = ProductTypeQuerySet

    def cached(self):
        return get_cached_data_or_set_new(
            key=settings.PRODUCT_TYPES_CACHE_KEY,
            callback=self.all,
            timeout=settings.PRODUCT_TYPES_CACHE_TIME,
        )

    def search(self, query):
        return self.filter(Q(name__icontains=query) | Q(description__icontains=query))
