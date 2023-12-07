from rest_framework import serializers

from api.v1.categories.models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "image",
            "name",
            "description",
            "views",
            "slug",
        )
        read_only_fields = ("views", "slug")


class DetailedCategorySerializer(CategorySerializer):
    calories_avg = serializers.IntegerField(
        source="product__nutrition__calories__avg", read_only=True
    )
    protein_avg = serializers.FloatField(
        source="product__nutrition__protein__avg", read_only=True
    )
    fat_avg = serializers.FloatField(
        source="product__nutrition__fat__avg", read_only=True
    )
    carbs_avg = serializers.FloatField(
        source="product__nutrition__carbs__avg", read_only=True
    )

    class Meta(CategorySerializer.Meta):
        fields = CategorySerializer.Meta.fields + (
            "calories_avg",
            "protein_avg",
            "fat_avg",
            "carbs_avg",
        )
