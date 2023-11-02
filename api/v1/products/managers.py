from django.db import models
from django.db.models import Avg, Count, Max, Min, QuerySet
from django.db.models.functions import Round

from api.v1.products.constants import PRICE_ROUNDING


class ProductQuerySet(models.QuerySet):
    def price_aggregation(self) -> dict[str, float]:
        """
        Returns the minimum, maximum, and average
        price of the QuerySet products.
        """
        return self.aggregate(
            price__min=Round(Min("price"), PRICE_ROUNDING),
            price__max=Round(Max("price"), PRICE_ROUNDING),
            price__avg=Round(Avg("price"), PRICE_ROUNDING),
        )


class ProductManager(models.Manager.from_queryset(ProductQuerySet)):
    ...


class ProductTypeQuerySet(models.QuerySet):
    def products_annotation(self) -> QuerySet:
        """
        Adds fields for the minimum, maximum, and
        average prices, as well as the count of
        stores offering products of the product_type
        to the QuerySet objects.
        """
        return self.annotate(
            product__price__avg=Round(Avg("product__price"), PRICE_ROUNDING),
            product__price__max=Round(Max("product__price"), PRICE_ROUNDING),
            product__price__min=Round(Min("product__price"), PRICE_ROUNDING),
            product__store__count=Count("product__store", distinct=True),
        )


class ProductTypeManager(models.Manager.from_queryset(ProductTypeQuerySet)):
    ...
