from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from comparisons.models import Comparison
from products.models import Product, ProductType


class ComparisonModifyService:
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


class ComparisonListService:
    def __init__(self, user):
        self.user = user

    def product_types_list(self):
        product_types = Comparison.objects.product_types(self.user)
        return product_types.product_price_annotation()

    def products_list(self, product_type_slug):
        product_type = get_object_or_404(ProductType, slug=product_type_slug)
        return Comparison.objects.products(product_type, self.user)
