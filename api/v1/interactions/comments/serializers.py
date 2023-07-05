from rest_framework import serializers

from api.v1.products.serializers import ProductModelSerializer
from api.v1.stores.serializers import StoreModelSerializer
from api.v1.users.serializers import UserModelSerializer
from interactions.comments.models import ProductComment, StoreComment
from products.models import Product
from stores.models import Store


class BaseCommentModelSerializer(serializers.ModelSerializer):
    author = UserModelSerializer(read_only=True)

    class Meta:
        fields = (
            "id",
            "author",
            "text",
            "created_at",
        )
        read_only_fields = ("created_at",)


class StoreCommentModelSerializer(BaseCommentModelSerializer):
    store = StoreModelSerializer(read_only=True)
    store_slug = serializers.SlugRelatedField(
        write_only=True,
        queryset=Store.objects.all(),
        slug_field="slug",
    )

    class Meta(BaseCommentModelSerializer.Meta):
        model = StoreComment
        fields = BaseCommentModelSerializer.Meta.fields + ("store", "store_slug")


class ProductCommentModelSerializer(BaseCommentModelSerializer):
    product = ProductModelSerializer(read_only=True)
    product_slug = serializers.SlugRelatedField(
        write_only=True,
        queryset=Product.objects.all(),
        slug_field="slug",
    )

    class Meta(BaseCommentModelSerializer.Meta):
        model = ProductComment
        fields = BaseCommentModelSerializer.Meta.fields + ("product", "product_slug")
