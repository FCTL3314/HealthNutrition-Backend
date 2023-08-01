from django.db import models

from products.models import ProductType


class ComparisonManager(models.Manager):
    @staticmethod
    def product_types(user):
        product_type_ids = user.comparison_set.values_list(
            "product__product_type", flat=True
        )
        return ProductType.objects.filter(id__in=product_type_ids.distinct())

    @staticmethod
    def products(product_type, user):
        return product_type.product_set.filter(user=user)
