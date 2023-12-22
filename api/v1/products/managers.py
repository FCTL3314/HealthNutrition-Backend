from django.db import models
from django.db.models import F, Sum, FloatField

from api.v1.products.constants import NutritionHealthfulnessCoefficient


class ProductQuerySet(models.QuerySet):
    def with_healthfulness(self):
        return self.annotate(
            healthfulness=(
                Sum(
                    (
                        F("nutrition__protein")
                        * NutritionHealthfulnessCoefficient.PROTEIN
                    )
                    + (F("nutrition__fat") * NutritionHealthfulnessCoefficient.FAT)
                    + (
                        F("nutrition__calories")
                        * NutritionHealthfulnessCoefficient.CALORIES
                    )
                    + (F("nutrition__carbs") * NutritionHealthfulnessCoefficient.CARBS),
                    output_field=FloatField(),
                )
            )
        )


class ProductManager(models.Manager.from_queryset(ProductQuerySet)):
    ...
