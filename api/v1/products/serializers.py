from rest_framework import serializers

from api.v1.products.models import Product, ProductType
from api.v1.stores.models import Store
from api.v1.stores.serializers import StoreModelSerializer


class ProductTypeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = (
            "id",
            "name",
            "description",
            "image",
            "views",
            "slug",
        )
        read_only_fields = ("views", "slug")


class ProductTypeAggregatedSerializer(ProductTypeModelSerializer):
    product_price_max = serializers.FloatField(
        source="product__price__max", required=False
    )
    product_price_avg = serializers.FloatField(
        source="product__price__avg", required=False
    )
    product_price_min = serializers.FloatField(
        source="product__price__min", required=False
    )
    product_stores_count = serializers.IntegerField(
        source="product__store__count", required=False
    )

    class Meta(ProductTypeModelSerializer.Meta):
        fields = ProductTypeModelSerializer.Meta.fields + (
            "product_price_max",
            "product_price_avg",
            "product_price_min",
            "product_stores_count",
        )
        read_only_fields = ProductTypeModelSerializer.Meta.read_only_fields + (
            "product_price_max",
            "product_price_avg",
            "product_price_min",
            "product_stores_count",
        )


class ProductModelSerializer(serializers.ModelSerializer):
    product_type = ProductTypeModelSerializer(read_only=True)
    product_type_id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=ProductType.objects.all(),
        source="product_type",
    )
    store = StoreModelSerializer(read_only=True)
    store_id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=Store.objects.all(),
        source="store",
    )

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "price",
            "card_description",
            "description",
            "image",
            "created_at",
            "updated_at",
            "store",
            "store_id",
            "product_type",
            "product_type_id",
            "views",
            "slug",
        )
        read_only_fields = (
            "created_at",
            "updated_at",
            "views",
            "slug",
        )
