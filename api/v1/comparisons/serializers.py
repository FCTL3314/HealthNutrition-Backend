from django.contrib.auth import get_user_model
from rest_framework import serializers

from api.v1.comparisons.models import Comparison, ComparisonGroup
from api.v1.products.models import Product
from api.v1.products.serializers import ProductSerializer
from api.v1.users.serializers import UserSerializer

User = get_user_model()


class ComparisonGroupSerializer(serializers.ModelSerializer):
    is_contains_selected_product = serializers.BooleanField(required=False)

    class Meta:
        model = ComparisonGroup
        fields = (
            "id",
            "name",
            "author_id",
            "created_at",
            "is_contains_selected_product",
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
