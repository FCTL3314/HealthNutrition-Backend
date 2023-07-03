from rest_framework import serializers

from api.v1.stores.serializers import StoreModelSerializer
from products.models import Product, ProductType
from stores.models import Store


class ProductTypeModelSerializer(serializers.ModelSerializer):
    product_price_max = serializers.FloatField(
        source="product__price__max", required=False
    )
    product_price_avg = serializers.FloatField(
        source="product__price__avg", required=False
    )
    product_price_min = serializers.FloatField(
        source="product__price__min", required=False
    )

    class Meta:
        model = ProductType
        fields = (
            "id",
            "name",
            "description",
            "image",
            "views",
            "slug",
            "product_price_max",
            "product_price_avg",
            "product_price_min",
        )
        read_only_fields = (
            "views",
            "slug",
            "product_price_max",
            "product_price_avg",
            "product_price_min",
        )


class ProductModelSerializer(serializers.ModelSerializer):
    product_type = ProductTypeModelSerializer(read_only=True)
    product_type_id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=ProductType.objects.all(),
    )
    store = StoreModelSerializer(read_only=True)
    store_id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=Store.objects.all(),
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
