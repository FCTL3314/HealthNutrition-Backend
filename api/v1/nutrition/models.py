from django.db import models


class Nutrition(models.Model):
    calories = models.PositiveIntegerField()
    protein = models.DecimalField(max_digits=5, decimal_places=2)
    fat = models.DecimalField(max_digits=5, decimal_places=2)
    carbs = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.calories=} g. | {self.protein=} g. | {self.fat=} g. | {self.carbs=} g."
