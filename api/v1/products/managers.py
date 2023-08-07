from django.db import models
from django.db.models import Avg, Count, Max, Min, Q, QuerySet
from django.db.models.functions import Round

from api.v1.products.constants import PRICE_ROUNDING


class ProductQuerySet(models.QuerySet):
    def price_aggregation(self) -> dict:
        aggregations = self.aggregate(
            price__min=Round(Min("price"), PRICE_ROUNDING),
            price__max=Round(Max("price"), PRICE_ROUNDING),
            price__avg=Round(Avg("price"), PRICE_ROUNDING),
        )
        return aggregations


class ProductManager(models.Manager):
    _queryset_class = ProductQuerySet

    def search(self, query: str) -> QuerySet:
        return self.filter(
            Q(name__icontains=query) | Q(card_description__icontains=query)
        )


class ProductTypeQuerySet(models.QuerySet):
    def product_price_annotation(self) -> QuerySet:
        return self.annotate(
            product__price__avg=Round(Avg("product__price"), PRICE_ROUNDING),
            product__price__max=Round(Max("product__price"), PRICE_ROUNDING),
            product__price__min=Round(Min("product__price"), PRICE_ROUNDING),
            product__store__count=Count("product__store", distinct=True),
        )


class ProductTypeManager(models.Manager):
    _queryset_class = ProductTypeQuerySet

    def search(self, query: str) -> QuerySet:
        return self.filter(Q(name__icontains=query) | Q(description__icontains=query))
