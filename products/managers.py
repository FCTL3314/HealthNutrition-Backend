from django.conf import settings
from django.db import models
from django.db.models import Avg, Count, Max, Min, Q
from django.db.models.functions import Round


class ProductQueryset(models.QuerySet):

    def price_aggregation(self):
        return self.aggregate(
            min_price=Round(Min('price'), settings.PRICE_ROUNDING),
            max_price=Round(Max('price'), settings.PRICE_ROUNDING),
            avg_price=Round(Avg('price'), settings.PRICE_ROUNDING),
        )


class ProductManager(models.Manager):
    _queryset_class = ProductQueryset

    def search(self, query):
        return self.filter(Q(name__icontains=query) | Q(card_description__icontains=query))


class ProductTypeQuerySet(models.QuerySet):

    def product_statistic_annotation(self):
        return self.annotate(
            product__price__avg=Round(Avg('product__price'), settings.PRICE_ROUNDING),
            product__price__max=Round(Max('product__price'), settings.PRICE_ROUNDING),
            product__price__min=Round(Min('product__price'), settings.PRICE_ROUNDING),
            product__store__count=Count('product__store', distinct=True),
        )


class ProductTypeManager(models.Manager):
    _queryset_class = ProductTypeQuerySet

    def popular(self):
        return self.order_by('-views')

    def search(self, query):
        return self.filter(Q(name__icontains=query) | Q(description__icontains=query))
