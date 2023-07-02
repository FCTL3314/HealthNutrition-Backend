from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from api.v1.products.paginators import ProductPageNumberPagination, ProductTypePageNumberPagination
from api.v1.products.serializers import ProductTypeModelSerializer, ProductModelSerializer
from common.decorators import order_queryset
from products.models import ProductType


class ComparisonProductTypeListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductTypeModelSerializer
    pagination_class = ProductTypePageNumberPagination
    ordering = settings.PRODUCT_TYPES_ORDERING

    @order_queryset(*ordering)
    def get_queryset(self):
        product_types = self.request.user.comparison_set.product_types()
        return product_types.product_price_annotation()


class ComparisonProductListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductModelSerializer
    pagination_class = ProductPageNumberPagination
    ordering = settings.PRODUCTS_ORDERING

    @order_queryset(*ordering)
    def get_queryset(self):
        slug = self.kwargs.get("slug")
        product_type = get_object_or_404(ProductType, slug=slug)
        products = product_type.cached_products()
        return products.filter(user=self.request.user)
