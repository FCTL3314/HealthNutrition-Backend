from rest_framework import serializers

from api.v1.comments.models import BaseComment, ProductComment, StoreComment
from api.v1.products.models import Product
from api.v1.products.serializers import ProductSerializer
from api.v1.stores.models import Store
from api.v1.stores.serializers import StoreSerializer
from api.v1.users.serializers import UserSerializer


class BaseCommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        abstract = True
        model = BaseComment
        fields = ("id", "author", "text", "created_at", "edited")
        read_only_fields = ("created_at", "edited")


class ProductCommentSerializer(BaseCommentSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=Product.objects.all(),
        source="product",
    )

    class Meta(BaseCommentSerializer.Meta):
        model = ProductComment
        fields = BaseCommentSerializer.Meta.fields + ("product", "product_id")


class StoreCommentSerializer(BaseCommentSerializer):
    store = StoreSerializer(read_only=True)
    store_id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=Store.objects.all(),
        source="store",
    )

    class Meta(BaseCommentSerializer.Meta):
        model = StoreComment
        fields = BaseCommentSerializer.Meta.fields + ("store", "store_id")
