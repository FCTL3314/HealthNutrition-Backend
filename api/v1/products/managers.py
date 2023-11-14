from django.db import models
from django.db.models import F

from api.v1.products.constants import NutritionHealthfulnessImportance


class ProductQuerySet(models.QuerySet):
    def with_healthfulness(self):
        return self.annotate(
            healthfulness=(
                (F("nutrition__protein") * NutritionHealthfulnessImportance.PROTEIN)
                + (F("nutrition__fat") * NutritionHealthfulnessImportance.FAT)
                + F("nutrition__calories")
                - (F("nutrition__carbs") * NutritionHealthfulnessImportance.CARBS)
            )
        )


class ProductManager(models.Manager.from_queryset(ProductQuerySet)):
    ...
