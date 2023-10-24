from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet

from api.permissions import IsAdminOrReadOnly
from api.responses import APIResponse
from api.utils.network import get_client_address
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
from api.v1.products.services import (
    ProductViewsIncreaseService,
    ProductTypeViewsIncreaseService,
    ProductRetrieveService,
    ProductTypeRetrieveService,
)


class ProductTypeViewSet(ModelViewSet):
    queryset = ProductType.objects.products_annotation().order_by(
        *PRODUCT_TYPES_ORDERING
    )
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name", "description")
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = ProductTypeAggregatedSerializer
    pagination_class = ProductTypePageNumberPagination
    lookup_field = "slug"

    def retrieve(self, request: Request, *args, **kwargs) -> APIResponse:
        instance = self.get_object()
        return ProductTypeRetrieveService(
            instance,
            self.serializer_class,
            ProductTypeViewsIncreaseService(instance, get_client_address(request)),
        ).retrieve()


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.order_by(*PRODUCTS_ORDERING)
    filterset_class = ProductFilter
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
    )
    search_fields = ("name", "card_description")
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = ProductSerializer
    pagination_class = ProductPageNumberPagination
    lookup_field = "slug"

    def retrieve(self, request: Request, *args, **kwargs) -> APIResponse:
        instance = self.get_object()
        return ProductRetrieveService(
            instance,
            self.serializer_class,
            ProductViewsIncreaseService(instance, get_client_address(request)),
        ).retrieve()
