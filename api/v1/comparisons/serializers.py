from rest_framework import serializers

from api.v1.products.serializers import ProductModelSerializer
from api.v1.users.serializers import UserModelSerializer
from comparisons.models import Comparison


class ComparisonModelSerializer(serializers.ModelSerializer):
    user = UserModelSerializer(read_only=True)
    product = ProductModelSerializer(read_only=True)

    class Meta:
        model = Comparison
        fields = ("user", "product")
