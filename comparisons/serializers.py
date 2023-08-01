from rest_framework import serializers

from comparisons.models import Comparison
from products.serializers import ProductModelSerializer
from users.serializers import UserSerializer


class ComparisonModelSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    product = ProductModelSerializer(read_only=True)

    class Meta:
        model = Comparison
        fields = ("user", "product")
