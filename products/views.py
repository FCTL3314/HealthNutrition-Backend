from common.permissions import IsAdminOrReadOnly
from django.conf import settings
from rest_framework.viewsets import ModelViewSet

from common.decorators import order_queryset
from products.filters import ProductFilter
from products.models import Product, ProductType
from products.paginators import (ProductPageNumberPagination,
                                 ProductTypePageNumberPagination)
from products.serializers import (ProductModelSerializer,
                                  ProductTypeModelSerializer)


class ProductTypeModelViewSet(ModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = ProductTypeModelSerializer
    pagination_class = ProductTypePageNumberPagination
    lookup_field = "slug"

    @order_queryset(*settings.PRODUCT_TYPES_ORDERING)
    def get_queryset(self):
        initial_queryset = ProductType.objects.cached()
        return initial_queryset.product_price_annotation()


class ProductModelViewSet(ModelViewSet):
    queryset = Product.objects.order_by(*settings.PRODUCTS_ORDERING)
    filterset_class = ProductFilter
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = ProductModelSerializer
    pagination_class = ProductPageNumberPagination
    lookup_field = "slug"
