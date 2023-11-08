from django.db import models


class DietType(models.Model):
    name = models.CharField(max_length=64)


class Diet(models.Model):
    name = models.CharField(max_length=64)
    diet_type = models.ForeignKey(to="diets.DietType", on_delete=models.PROTECT)
    user = models.ForeignKey(to="users.User", on_delete=models.CASCADE)


class MealTimes(models.Choices):
    breakfast = "breakfast"
    lunch = "lunch"
    dinner = "dinner"


class DietProduct(models.Model):
    mealtime = models.CharField(max_length=32, choices=MealTimes.choices)
    proportional_ratio = models.DecimalField(max_digits=5, decimal_places=2)
    product = models.ForeignKey(to="products.Product", on_delete=models.CASCADE)
    diet = models.ForeignKey(to="diets.Diet", on_delete=models.CASCADE)
