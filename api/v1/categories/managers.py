from django.db import models
from django.db.models import Avg


class CategoryQuerySet(models.QuerySet):
    def with_nutrition_averages(self):
        return self.annotate(
            Avg("product__nutrition__calories"),
            Avg("product__nutrition__protein"),
            Avg("product__nutrition__fat"),
            Avg("product__nutrition__carbs"),
        )


class CategoryManager(models.Manager.from_queryset(CategoryQuerySet)):
    ...
