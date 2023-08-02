from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from api.v1.comparisons.models import Comparison
from api.v1.comparisons.serializers import ComparisonModelSerializer
from api.v1.products.models import Product, ProductType
from api.v1.users.models import User
from common.decorators import order_queryset


class ComparisonModifyService:
    serializer_class = ComparisonModelSerializer

    def __init__(self, product_id: int, user: User):
        self.product_id = product_id
        self.user = user

    def add(self) -> Response:
        product = get_object_or_404(Product, pk=self.product_id)
        self.user.comparisons.add(product, through_defaults=None)
        serializer = self.serializer_class(
            get_object_or_404(Comparison, product=product, user=self.user),
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def remove(self) -> Response:
        product = get_object_or_404(Product, pk=self.product_id, user=self.user)
        self.user.comparisons.remove(product)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ComparisonListService:
    def __init__(self, user: User):
        self.user = user

    @order_queryset(*settings.PRODUCT_TYPES_ORDERING)
    def product_types_list(self):
        product_types = Comparison.objects.product_types(self.user)
        return product_types.product_price_annotation()

    @order_queryset(*settings.PRODUCTS_ORDERING)
    def products_list(self, product_type_slug: str):
        product_type = get_object_or_404(ProductType, slug=product_type_slug)
        return Comparison.objects.products(product_type, self.user)
