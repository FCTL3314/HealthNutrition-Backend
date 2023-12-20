from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import (
    Exists,
    OuterRef,
    Count,
    Max,
    Avg,
    Subquery,
    When,
    Value,
    Case,
    IntegerField,
)

from api.v1.comparisons.services.models import (
    get_comparison_model,
)
from api.v1.products.models import Product

User = get_user_model()


class ComparisonGroupQuerySet(models.QuerySet):
    def for_user(self, user: User):
        return self.filter(author=user)

    def newest_first_order(self):
        return self.order_by("-created_at")

    def position_order(self):
        return self.order_by("position")

    def with_is_contains_selected_product(self, selected_product_id: int):
        return self.annotate(
            is_contains_selected_product=Exists(
                get_comparison_model()  # noqa
                .objects.filter(
                    comparison_group=OuterRef("pk"), product=selected_product_id
                )
                .values("comparison_group")
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

    def with_standout_products(self):
        def product_with_specific_nutrition_subquery(order_by: str) -> Subquery:
            return Subquery(
                get_comparison_model()  # noqa
                .objects.filter(comparison_group=OuterRef("pk"))
                .order_by(order_by)
                .values_list("product__slug", flat=True)[:1]
            )

        return self.annotate(
            max_calorie_product_slug=product_with_specific_nutrition_subquery(
                "-product__nutrition__calories"
            ),
            min_calorie_product_slug=product_with_specific_nutrition_subquery(
                "product__nutrition__calories"
            ),
            max_protein_product_slug=product_with_specific_nutrition_subquery(
                "-product__nutrition__protein"
            ),
            min_protein_product_slug=product_with_specific_nutrition_subquery(
                "product__nutrition__protein"
            ),
            max_fat_product_slug=product_with_specific_nutrition_subquery(
                "-product__nutrition__fat"
            ),
            min_fat_product_slug=product_with_specific_nutrition_subquery(
                "product__nutrition__fat"
            ),
            max_carbs_product_slug=product_with_specific_nutrition_subquery(
                "-product__nutrition__carbs"
            ),
            min_carbs_product_slug=product_with_specific_nutrition_subquery(
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
    def update_position_order(self, ordered_ids: list[int]) -> None:
        comparison_groups = self.filter(id__in=ordered_ids)  # noqa

        if len(comparison_groups) != len(ordered_ids):
            raise ValueError("One or more provided ids do not exist in the database.")

        when_statements = [
            When(id=group_id, then=Value(new_position))
            for new_position, group_id in enumerate(ordered_ids)
        ]
        case_expression = Case(
            *when_statements,
            output_field=IntegerField(),
        )

        comparison_groups.update(position=case_expression)


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
