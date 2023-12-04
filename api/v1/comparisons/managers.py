from django.apps import apps
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import (
    Exists,
    OuterRef,
    Count,
    Max,
    Avg,
    Min,
)

from api.v1.products.models import Product

User = get_user_model()


class ComparisonGroupQuerySet(models.QuerySet):
    def for_user(self, user: User):
        return self.filter(author=user)

    def newest(self):
        return self.order_by("-created_at")

    def with_is_contains_selected_product(self, selected_product_id: int):
        comparison_model = apps.get_model(
            app_label="comparisons", model_name="Comparison"
        )
        return self.annotate(
            is_contains_selected_product=Exists(
                comparison_model.objects.filter(  # noqa
                    comparison_group=OuterRef("pk"), product=selected_product_id
                ).values("comparison_group")
            )
        )

    def with_products_count(self):
        return self.annotate(products_count=Count("comparisons__product"))

    def with_nutrition_details(self):
        return self.annotate(
            Max("comparisons__product__nutrition__calories"),
            Max("comparisons__product__nutrition__protein"),
            Max("comparisons__product__nutrition__fat"),
            Max("comparisons__product__nutrition__carbs"),
            Avg("comparisons__product__nutrition__calories"),
            Avg("comparisons__product__nutrition__protein"),
            Avg("comparisons__product__nutrition__fat"),
            Avg("comparisons__product__nutrition__carbs"),
            Min("comparisons__product__nutrition__calories"),
            Min("comparisons__product__nutrition__protein"),
            Min("comparisons__product__nutrition__fat"),
            Min("comparisons__product__nutrition__carbs"),
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
