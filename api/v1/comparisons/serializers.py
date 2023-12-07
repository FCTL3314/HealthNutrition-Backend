from django.contrib.auth import get_user_model
from rest_framework import serializers

from api.v1.comparisons.models import Comparison, ComparisonGroup
from api.v1.products.models import Product
from api.v1.products.serializers import ProductSerializer
from api.v1.users.serializers import UserSerializer

User = get_user_model()


class ComparisonGroupReadSerializer(serializers.Serializer):
    selected_product = serializers.PrimaryKeyRelatedField(
        required=False, queryset=Product.objects.all()
    )
    with_products_count = serializers.BooleanField()


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
        read_only_fields = ("slug",)


class DetailedComparisonGroupSerializer(ComparisonGroupSerializer):
    is_contains_selected_product = serializers.BooleanField(read_only=True)
    products_count = serializers.IntegerField(read_only=True)
    unique_categories_count = serializers.IntegerField(read_only=True)
    last_added_product_datetime = serializers.DateTimeField(read_only=True)
    max_calorie_product_slug = serializers.SlugField(read_only=True)
    min_calorie_product_slug = serializers.SlugField(read_only=True)
    max_protein_product_slug = serializers.SlugField(read_only=True)
    min_protein_product_slug = serializers.SlugField(read_only=True)
    max_fat_product_slug = serializers.SlugField(read_only=True)
    min_fat_product_slug = serializers.SlugField(read_only=True)
    max_carbs_product_slug = serializers.SlugField(read_only=True)
    min_carbs_product_slug = serializers.SlugField(read_only=True)

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

    class Meta(ComparisonGroupSerializer.Meta):
        fields = ComparisonGroupSerializer.Meta.fields + (
            "unique_categories_count",
            "last_added_product_datetime",
            "calories_avg",
            "protein_avg",
            "fat_avg",
            "carbs_avg",
            "max_calorie_product_slug",
            "min_calorie_product_slug",
            "max_protein_product_slug",
            "min_protein_product_slug",
            "max_fat_product_slug",
            "min_fat_product_slug",
            "max_carbs_product_slug",
            "min_carbs_product_slug",
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
