from rest_framework.viewsets import ModelViewSet

from api.decorators import order_queryset
from api.permissions import IsAdminOrReadOnly
from api.v1.products.constants import (PRODUCT_TYPES_ORDERING,
                                       PRODUCTS_ORDERING)
from api.v1.products.filters import ProductFilter
from api.v1.products.models import Product, ProductType
from api.v1.products.paginators import (ProductPageNumberPagination,
                                        ProductTypePageNumberPagination)
from api.v1.products.serializers import (ProductModelSerializer,
                                         ProductTypeAggregatedSerializer)


class ProductTypeModelViewSet(ModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = ProductTypeAggregatedSerializer
    pagination_class = ProductTypePageNumberPagination
    lookup_field = "slug"

    @order_queryset(*PRODUCT_TYPES_ORDERING)
    def get_queryset(self):
        initial_queryset = ProductType.objects.all()
        return initial_queryset.product_price_annotation()


class ProductModelViewSet(ModelViewSet):
    queryset = Product.objects.order_by(*PRODUCTS_ORDERING)
    filterset_class = ProductFilter
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = ProductModelSerializer
    pagination_class = ProductPageNumberPagination
    lookup_field = "slug"
