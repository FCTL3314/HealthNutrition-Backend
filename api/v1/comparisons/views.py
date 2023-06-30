from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from api.v1.products.paginators import ProductPageNumberPagination, ProductTypePageNumberPagination
from api.v1.products.serializers import ProductTypeModelSerializer, ProductModelSerializer
from comparisons.models import Comparison
from products.models import ProductType


# TODO: Rewrite

class ComparisonProductTypeModelViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductTypeModelSerializer
    pagination_class = ProductTypePageNumberPagination
    lookup_field = "slug"

    def get_queryset(self):
        product_types = self.request.user.comparison_set.product_types()
        queryset = product_types.product_price_annotation()
        return queryset.order_by(*settings.PRODUCT_TYPES_ORDERING)


class ComparisonProductGenericViewSet(GenericViewSet, ListModelMixin):
    model = Comparison
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductModelSerializer
    pagination_class = ProductPageNumberPagination
    lookup_field = "slug"

    def list(self, request, *args, **kwargs):
        slug = self.request.query_params.get("product_type_slug")
        if not slug:
            return Response({"product_type_slug": "This field is required."}, status=status.HTTP_400_BAD_REQUEST)
        product_type = get_object_or_404(ProductType, slug=slug)
        products = product_type.cached_products()
        queryset = products.filter(user=self.request.user).order_by(*settings.PRODUCTS_ORDERING)
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = self.serializer_class(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)
