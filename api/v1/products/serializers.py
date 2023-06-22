from rest_framework import serializers

from api.v1.stores.serializers import StoreModelSerializer
from products.models import Product, ProductType
from stores.models import Store


class ProductTypeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = ("id", "name", "description", "image", "views", "slug")
        read_only_fields = ("views", "slug")


class ProductModelSerializer(serializers.ModelSerializer):
    store = StoreModelSerializer(read_only=True)
    product_type = ProductTypeModelSerializer(read_only=True)
    product_type_id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=ProductType.objects.all(),
        source='product_type',
    )
    store_id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=Store.objects.all(),
        source='store',
    )

    class Meta:
        model = Product
        fields = (
            "id", "name", "price", "card_description", "description", "image", "created_at", "updated_at", "store",
            "store_id", "product_type", "product_type_id", "views", "slug"
        )
        read_only_fields = ("created_at", "updated_at", "views", "slug")
