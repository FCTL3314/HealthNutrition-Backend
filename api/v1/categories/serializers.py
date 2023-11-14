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


class CategoryDetailedSerializer(CategorySerializer):
    calories_max = serializers.IntegerField(
        source="product__nutrition__calories__max", read_only=True
    )
    protein_max = serializers.FloatField(
        source="product__nutrition__protein__max", read_only=True
    )
    fat_max = serializers.FloatField(
        source="product__nutrition__fat__max", read_only=True
    )
    carbs_max = serializers.FloatField(
        source="product__nutrition__carbs__max", read_only=True
    )

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

    calories_min = serializers.IntegerField(
        source="product__nutrition__calories__min", read_only=True
    )
    protein_min = serializers.FloatField(
        source="product__nutrition__protein__min", read_only=True
    )
    fat_min = serializers.FloatField(
        source="product__nutrition__fat__min", read_only=True
    )
    carbs_min = serializers.FloatField(
        source="product__nutrition__carbs__min", read_only=True
    )

    class Meta(CategorySerializer.Meta):
        fields = CategorySerializer.Meta.fields + (
            "calories_max",
            "protein_max",
            "fat_max",
            "carbs_max",
            "calories_avg",
            "protein_avg",
            "fat_avg",
            "carbs_avg",
            "calories_min",
            "protein_min",
            "fat_min",
            "carbs_min",
        )
