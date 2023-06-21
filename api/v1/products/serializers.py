from rest_framework import serializers

from products.models import ProductType


class ProductTypeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = ("id", "name", "description", "image", "views", "slug")
