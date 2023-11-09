from django.contrib.auth import get_user_model
from django.db import models

from api.v1.products.models import Product

User = get_user_model()


class ComparisonQuerySet(models.QuerySet):
    def products(self, comparison_group_id: int):
        product_ids = self.filter(comparison_group__id=comparison_group_id).values_list(
            "product", flat=True
        )
        return Product.objects.filter(id__in=product_ids)


class ComparisonManager(models.Manager.from_queryset(ComparisonQuerySet)):
    ...
