from django.db import models

from api.v1.products.models import ProductType
from api.v1.users.models import User


class ComparisonManager(models.Manager):
    @staticmethod
    def product_types(user: User):
        product_type_ids = user.comparison_set.values_list(
            "product__product_type", flat=True
        )
        return ProductType.objects.filter(id__in=product_type_ids.distinct())

    @staticmethod
    def products(product_type: ProductType, user: User):
        return product_type.product_set.filter(user=user)
