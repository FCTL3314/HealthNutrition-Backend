from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from common.decorators import order_queryset
from comparisons.serializers import ComparisonModelSerializer
from comparisons.services import ComparisonService
from products.models import ProductType
from products.paginators import (
    ProductPageNumberPagination,
    ProductTypePageNumberPagination,
)
from products.serializers import ProductModelSerializer, ProductTypeAggregatedSerializer


class ComparisonProductTypeListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductTypeAggregatedSerializer
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


class ComparisonGenericViewSet(GenericViewSet, CreateModelMixin, DestroyModelMixin):
    permission_classes = (IsAuthenticated,)
    serializer_class = ComparisonModelSerializer

    @property
    def comparison_service(self):
        return ComparisonService(self.kwargs["product_id"])

    def create(self, request, *args, **kwargs):
        return self.comparison_service.add(request.user, self.serializer_class)

    def destroy(self, request, *args, **kwargs):
        return self.comparison_service.remove(request.user)
