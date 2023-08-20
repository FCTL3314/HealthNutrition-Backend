from rest_framework import serializers

from api.v1.comparisons.models import Comparison
from api.v1.products.serializers import ProductSerializer
from api.v1.users.serializers import UserSerializer


class ComparisonSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Comparison
        fields = ("user", "product")
