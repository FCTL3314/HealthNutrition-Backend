from django.conf import settings
from django.db import models
from django.db.models import Avg, Count, Max, Min
from django.db.models.functions import Round


class ProductTypeManager(models.Manager):

    def popular(self):
        return self.order_by('-views')

    @staticmethod
    def annotate_products_statistic(queryset):
        return queryset.annotate(
            product__price__avg=Round(Avg('product__price'), settings.PRICE_ROUNDING),
            product__price__max=Round(Max('product__price'), settings.PRICE_ROUNDING),
            product__price__min=Round(Min('product__price'), settings.PRICE_ROUNDING),
            product__store__count=Count('product__store', distinct=True),
        )
