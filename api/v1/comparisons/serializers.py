from django.contrib.auth import get_user_model
from rest_framework import serializers

from api.v1.comparisons.models import Comparison, ComparisonGroup
from api.v1.products.models import Product
from api.v1.products.serializers import ProductSerializer
from api.v1.users.serializers import UserSerializer

User = get_user_model()


class ComparisonGroupReadSerializer(serializers.Serializer):
    selected_product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        required=False,
    )
    with_products_count = serializers.BooleanField(required=False)


class ComparisonGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComparisonGroup
        fields = (
            "id",
            "name",
            "author_id",
            "created_at",
            "slug",
        )


class DetailedComparisonGroupSerializer(ComparisonGroupSerializer):
    is_contains_selected_product = serializers.BooleanField(
        required=False, read_only=True
    )
    products_count = serializers.IntegerField(required=False, read_only=True)
    calories_max = serializers.IntegerField(
        source="comparisons__product__nutrition__calories__max", read_only=True
    )
    protein_max = serializers.FloatField(
        source="comparisons__product__nutrition__protein__max", read_only=True
    )
    fat_max = serializers.FloatField(
        source="comparisons__product__nutrition__fat__max", read_only=True
    )
    carbs_max = serializers.FloatField(
        source="comparisons__product__nutrition__carbs__max", read_only=True
    )

    calories_avg = serializers.IntegerField(
        source="comparisons__product__nutrition__calories__avg", read_only=True
    )
    protein_avg = serializers.FloatField(
        source="comparisons__product__nutrition__protein__avg", read_only=True
    )
    fat_avg = serializers.FloatField(
        source="comparisons__product__nutrition__fat__avg", read_only=True
    )
    carbs_avg = serializers.FloatField(
        source="comparisons__product__nutrition__carbs__avg", read_only=True
    )

    calories_min = serializers.IntegerField(
        source="comparisons__product__nutrition__calories__min", read_only=True
    )
    protein_min = serializers.FloatField(
        source="comparisons__product__nutrition__protein__min", read_only=True
    )
    fat_min = serializers.FloatField(
        source="comparisons__product__nutrition__fat__min", read_only=True
    )
    carbs_min = serializers.FloatField(
        source="comparisons__product__nutrition__carbs__min", read_only=True
    )

    class Meta(ComparisonGroupSerializer.Meta):
        fields = ComparisonGroupSerializer.Meta.fields + (
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
            "is_contains_selected_product",
            "products_count",
        )


class ComparisonReadSerializer(serializers.ModelSerializer):
    comparison_group_id = serializers.PrimaryKeyRelatedField(
        queryset=ComparisonGroup.objects.all(),
        source="comparison_group",
        required=True,
    )

    class Meta:
        model = Comparison
        fields = ("comparison_group_id",)


class ComparisonSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source="product",
        write_only=True,
        required=True,
    )
    comparison_group_id = serializers.PrimaryKeyRelatedField(
        queryset=ComparisonGroup.objects.all(),
        source="comparison_group",
        write_only=True,
        required=True,
    )

    class Meta:
        model = Comparison
        fields = ("user", "product", "product_id", "comparison_group_id")
