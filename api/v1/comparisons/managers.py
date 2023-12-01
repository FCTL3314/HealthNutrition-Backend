from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Case, When, Value, BooleanField

from api.v1.products.models import Product

User = get_user_model()


class ComparisonGroupQuerySet(models.QuerySet):
    def newest(self):
        return self.order_by("-created_at")

    def with_is_contains_selected_product(self, selected_product_id: int):
        return self.annotate(
            is_contains_selected_product=Case(
                When(comparisons__product_id=selected_product_id, then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            )
        )


class ComparisonGroupManager(models.Manager.from_queryset(ComparisonGroupQuerySet)):
    ...


class ComparisonQuerySet(models.QuerySet):
    def products(self, comparison_group_id: int):
        product_ids = self.filter(comparison_group_id=comparison_group_id).values_list(
            "product", flat=True
        )
        return Product.objects.filter(id__in=product_ids)


class ComparisonManager(models.Manager.from_queryset(ComparisonQuerySet)):
    ...
