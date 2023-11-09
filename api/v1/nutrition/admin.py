from django.contrib import admin

from api.v1.nutrition.models import Nutrition


@admin.register(Nutrition)
class NutritionAdmin(admin.ModelAdmin):
    ordering = ("calories",)
