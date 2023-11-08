from rest_framework import serializers

from api.v1.nutrition.models import Nutrition


class NutritionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nutrition
        fields = ("id", "calories", "protein", "fat", "carbs")
