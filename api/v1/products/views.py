from rest_framework.viewsets import ModelViewSet

from api.permissions import IsAdminOrReadOnly
from api.v1.products.constants import PRODUCT_TYPES_ORDERING, PRODUCTS_ORDERING
from api.v1.products.filters import ProductFilter
from api.v1.products.models import Product, ProductType
from api.v1.products.paginators import (
    ProductPageNumberPagination,
    ProductTypePageNumberPagination,
)
from api.v1.products.serializers import (
    ProductSerializer,
    ProductTypeAggregatedSerializer,
)


class ProductTypeViewSet(ModelViewSet):
    queryset = ProductType.objects.products_annotation().order_by(
        *PRODUCT_TYPES_ORDERING
    )
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = ProductTypeAggregatedSerializer
    pagination_class = ProductTypePageNumberPagination
    lookup_field = "slug"


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.order_by(*PRODUCTS_ORDERING)
    filterset_class = ProductFilter
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = ProductSerializer
    pagination_class = ProductPageNumberPagination
    lookup_field = "slug"
