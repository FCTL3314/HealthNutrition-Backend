from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.v1.comparisons.serializers import ComparisonModelSerializer
from api.v1.products.paginators import (ProductPageNumberPagination,
                                        ProductTypePageNumberPagination)
from api.v1.products.serializers import (ProductModelSerializer,
                                         ProductTypeModelSerializer)
from common.decorators import order_queryset
from comparisons.models import Comparison
from products.models import Product, ProductType


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


class ComparisonGenericViewSet(GenericViewSet, CreateModelMixin, DestroyModelMixin):
    model = Comparison
    permission_classes = (IsAuthenticated,)
    serializer_class = ComparisonModelSerializer

    def create(self, request, *args, **kwargs):
        product = self.get_product()
        request.user.comparisons.add(product, through_defaults=None)
        serializer = self.get_serializer(
            get_object_or_404(Comparison, product=product, user=request.user),
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        product = self.get_product(user=request.user)
        request.user.comparisons.remove(product)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_product(self, **kwargs):
        return get_object_or_404(Product, pk=self.kwargs["product_id"], **kwargs)
