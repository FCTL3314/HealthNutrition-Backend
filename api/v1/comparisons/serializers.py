from rest_framework import serializers

from api.v1.comparisons.models import Comparison
from api.v1.products.serializers import ProductModelSerializer
from api.v1.users.serializers import UserSerializer


class ComparisonModelSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    product = ProductModelSerializer(read_only=True)

    class Meta:
        model = Comparison
        fields = ("user", "product")
