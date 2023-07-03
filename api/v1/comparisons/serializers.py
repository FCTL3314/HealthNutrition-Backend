from rest_framework import serializers

from api.v1.products.serializers import ProductModelSerializer
from comparisons.models import Comparison


class ComparisonModelSerializer(serializers.ModelSerializer):
    # TODO: UserModelSerializer
    product = ProductModelSerializer(read_only=True)

    class Meta:
        model = Comparison
        fields = ("user", "product")
        extra_kwargs = {
            "user": {"required": False},  # TODO: Remove
        }
