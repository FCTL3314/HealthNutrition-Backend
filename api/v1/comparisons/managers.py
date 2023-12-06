from django.apps import apps
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import (
    Exists,
    OuterRef,
    Count,
    Max,
    Avg,
    Subquery,
)

from api.v1.products.models import Product

User = get_user_model()


class ComparisonGroupQuerySet(models.QuerySet):
    def for_user(self, user: User):
        return self.filter(author=user)

    def newest_first_order(self):
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

    def with_last_added_product_datetime(self):
        return self.annotate(last_added_product_datetime=Max("comparisons__created_at"))

    def with_unique_categories_count(self):
        return self.annotate(
            unique_categories_count=Count(
                "comparisons__product__category", distinct=True
            )
        )

    def with_extreme_nutrition_products(self):
        comparison_model = apps.get_model(
            app_label="comparisons", model_name="Comparison"
        )

        def product_with_specific_nutrition_subquery(order_by: str):
            return Subquery(
                comparison_model.objects.filter(comparison_group=OuterRef("pk"))  # noqa
                .order_by(order_by)
                .values_list("product_id", flat=True)[:1]
            )

        return self.annotate(
            max_calorie_product_id=product_with_specific_nutrition_subquery(
                "-product__nutrition__calories"
            ),
            min_calorie_product_id=product_with_specific_nutrition_subquery(
                "product__nutrition__calories"
            ),
            max_protein_product_id=product_with_specific_nutrition_subquery(
                "-product__nutrition__protein"
            ),
            min_protein_product_id=product_with_specific_nutrition_subquery(
                "product__nutrition__protein"
            ),
            max_fat_product_id=product_with_specific_nutrition_subquery(
                "-product__nutrition__fat"
            ),
            min_fat_product_id=product_with_specific_nutrition_subquery(
                "product__nutrition__fat"
            ),
            max_carbs_product_id=product_with_specific_nutrition_subquery(
                "-product__nutrition__carbs"
            ),
            min_carbs_product_id=product_with_specific_nutrition_subquery(
                "product__nutrition__carbs"
            ),
        )

    def with_nutrition_details(self):
        return self.annotate(
            Avg("comparisons__product__nutrition__calories"),
            Avg("comparisons__product__nutrition__protein"),
            Avg("comparisons__product__nutrition__fat"),
            Avg("comparisons__product__nutrition__carbs"),
        )


class ComparisonGroupManager(models.Manager.from_queryset(ComparisonGroupQuerySet)):
    ...


class ComparisonQuerySet(models.QuerySet):
    def products(self, comparison_group_id: int):
        product_ids = self.filter(comparison_group_id=comparison_group_id).values_list(
            "product", flat=True
        )
        return Product.objects.select_related("nutrition", "category").filter(
            id__in=product_ids
        )


class ComparisonManager(models.Manager.from_queryset(ComparisonQuerySet)):
    ...
