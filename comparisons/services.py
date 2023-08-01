from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from comparisons.models import Comparison
from products.models import Product


class ComparisonService:
    def __init__(self, product_id):
        self.product_id = product_id

    def add(self, user, serializer_class):
        product = get_object_or_404(Product, pk=self.product_id)
        user.comparisons.add(product, through_defaults=None)
        serializer = serializer_class(
            get_object_or_404(Comparison, product=product, user=user),
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def remove(self, user):
        product = get_object_or_404(Product, pk=self.product_id, user=user)
        user.comparisons.remove(product)
        return Response(status=status.HTTP_204_NO_CONTENT)
