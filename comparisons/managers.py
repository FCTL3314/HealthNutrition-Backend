from django.db import models

from products.models import ProductType


class ComparisonManager(models.Manager):

    def product_types(self):
        product_types_ids = self.values_list('product__product_type', flat=True).distinct()
        return ProductType.objects.filter(id__in=product_types_ids)
