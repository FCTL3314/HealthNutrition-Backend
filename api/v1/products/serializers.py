from rest_framework import serializers

from api.v1.categories.models import Category
from api.v1.categories.serializers import CategorySerializer
from api.v1.nutrition.models import Nutrition
from api.v1.nutrition.serializers import NutritionSerializer
from api.v1.nutrition.services.infrastructure.humanized_calorie_burning_calculators import (
    CalorieBurningCalculatorForBasicExercises,
)
from api.v1.products.models import Product


class ProductReadSerializer(serializers.Serializer):
    body_weight = serializers.FloatField(write_only=True, required=False)


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=Category.objects.all(),
        source="category",
    )
    nutrition = NutritionSerializer(read_only=True)
    nutrition_id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=Nutrition.objects.all(),
        source="nutrition",
    )

    class Meta:
        model = Product
        fields = (
            "id",
            "image",
            "name",
            "description",
            "short_description",
            "category",
            "category_id",
            "nutrition",
            "nutrition_id",
            "views",
            "slug",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "created_at",
            "updated_at",
            "views",
            "slug",
        )


class ProductWithNutritionSerializer(ProductSerializer):
    healthfulness = serializers.IntegerField(read_only=True)

    class Meta(ProductSerializer.Meta):
        fields = ProductSerializer.Meta.fields + ("healthfulness",)


class ProductWithCaloriesBurningTimeSerializer(ProductSerializer):
    calories_burning_time = serializers.SerializerMethodField(read_only=True)

    class Meta(ProductSerializer.Meta):
        fields = ProductSerializer.Meta.fields + ("calories_burning_time",)

    def get_calories_burning_time(self, instance: Product) -> dict[str, str]:
        calories = instance.nutrition.calories
        body_weight = self.context.get("body_weight")
        if isinstance(body_weight, str):
            body_weight = float(body_weight)

        basic_exercises_calories_burning_calculator = (
            CalorieBurningCalculatorForBasicExercises(
                exercise_hours=1, body_weight=body_weight
            )
        )
        return {
            "walking": basic_exercises_calories_burning_calculator.calculate_walking(
                calories
            ),
            "running": basic_exercises_calories_burning_calculator.calculate_running(
                calories
            ),
            "cycling": basic_exercises_calories_burning_calculator.calculate_cycling(
                calories
            ),
        }


class DetailedProductSerializer(
    ProductWithNutritionSerializer, ProductWithCaloriesBurningTimeSerializer
):
    class Meta(ProductSerializer.Meta):
        fields = (
            ProductWithNutritionSerializer.Meta.fields
            + ProductWithCaloriesBurningTimeSerializer.Meta.fields
        )
