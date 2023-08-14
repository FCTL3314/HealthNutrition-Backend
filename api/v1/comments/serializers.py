from rest_framework import serializers

from api.v1.comments.models import BaseComment, ProductComment
from api.v1.products.models import Product
from api.v1.products.serializers import ProductModelSerializer
from api.v1.users.serializers import UserSerializer


class BaseCommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        abstract = True
        model = BaseComment
        fields = ("id", "author", "text", "created_at")
        read_only_fields = ("created_at",)


class ProductCommentSerializer(BaseCommentSerializer):
    product = ProductModelSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=Product.objects.all(),
        source="product",
    )

    class Meta(BaseCommentSerializer.Meta):
        model = ProductComment
        fields = BaseCommentSerializer.Meta.fields + ("product", "product_id")  # type: ignore[assignment]
