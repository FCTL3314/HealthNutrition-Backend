from django.db import models
from django.db.models import Avg, Max, Min


class CategoryQuerySet(models.QuerySet):
    def with_nutrition_details(self):
        return self.annotate(
            Max("product__nutrition__calories"),
            Max("product__nutrition__protein"),
            Max("product__nutrition__fat"),
            Max("product__nutrition__carbs"),
            Avg("product__nutrition__calories"),
            Avg("product__nutrition__protein"),
            Avg("product__nutrition__fat"),
            Avg("product__nutrition__carbs"),
            Min("product__nutrition__calories"),
            Min("product__nutrition__protein"),
            Min("product__nutrition__fat"),
            Min("product__nutrition__carbs"),
        )


class CategoryManager(models.Manager.from_queryset(CategoryQuerySet)):
    ...
