from rest_framework import serializers

from api.v1.categories.models import Category


class CategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "image",
            "name",
            "description",
            "views",
            "slug",
        )
        read_only_fields = ("views", "slug")
