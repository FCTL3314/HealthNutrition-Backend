from django.conf import settings
from rest_framework.viewsets import ModelViewSet

from api.permissions import IsAdminOrReadOnly
from api.v1.products.paginators import (ProductPageNumberPagination,
                                        ProductTypePageNumberPagination)
from api.v1.products.serializers import (ProductModelSerializer,
                                         ProductTypeModelSerializer)
from products.models import Product, ProductType


class ProductTypeModelViewSet(ModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = ProductTypeModelSerializer
    pagination_class = ProductTypePageNumberPagination
    lookup_field = "slug"

    def get_queryset(self):
        initial_queryset = ProductType.objects.cached()
        queryset = initial_queryset.product_price_annotation()
        return queryset.order_by(*settings.PRODUCT_TYPES_ORDERING)


class ProductModelViewSet(ModelViewSet):
    queryset = Product.objects.all().order_by(*settings.PRODUCTS_ORDERING)
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = ProductModelSerializer
    pagination_class = ProductPageNumberPagination
    lookup_field = "slug"
