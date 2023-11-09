from django.db import models


class Nutrition(models.Model):
    calories = models.PositiveIntegerField()
    protein = models.DecimalField(max_digits=5, decimal_places=2)
    fat = models.DecimalField(max_digits=5, decimal_places=2)
    carbs = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        verbose_name_plural = "Nutrition"

    def __str__(self):
        return (
            f"Calories: {self.calories} g. "
            f"Protein: {self.protein} g. "
            f"Fat: {self.fat} g. "
            f"Carbs: {self.carbs} g."
        )
