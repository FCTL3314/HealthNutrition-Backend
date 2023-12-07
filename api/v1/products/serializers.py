from rest_framework import serializers

from api.v1.categories.models import Category
from api.v1.categories.serializers import CategorySerializer
from api.v1.nutrition.models import Nutrition
from api.v1.nutrition.serializers import NutritionSerializer
from api.v1.products.models import Product


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
            "short_description",
            "nutrition",
            "nutrition_id",
            "category",
            "category_id",
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


class DetailProductSerializer(ProductSerializer):
    healthfulness = serializers.IntegerField(read_only=True)

    class Meta(ProductSerializer.Meta):
        fields = ProductSerializer.Meta.fields + ("healthfulness",)
