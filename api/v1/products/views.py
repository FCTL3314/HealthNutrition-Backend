from http import HTTPStatus

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet

from api.common.permissions import IsAdminOrReadOnly
from api.responses import APIResponse
from api.utils.network import get_client_address
from api.v1.products.constants import PRODUCTS_ORDERING
from api.v1.products.filters import ProductFilter
from api.v1.products.models import Product
from api.v1.products.paginators import (
    ProductPageNumberPagination,
)
from api.v1.products.serializers import (
    ProductWithHealthfulnessSerializer,
)
from api.v1.products.services import (
    ProductViewsIncreaseService,
)


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.with_healthfulness().order_by(*PRODUCTS_ORDERING)
    filterset_class = ProductFilter
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
    )
    search_fields = ("name", "short_description")
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = ProductWithHealthfulnessSerializer
    pagination_class = ProductPageNumberPagination
    lookup_field = "slug"

    def retrieve(self, request: Request, *args, **kwargs) -> APIResponse:
        instance = self.get_object()
        ProductViewsIncreaseService(instance, get_client_address(request)).execute()
        serializer = self.get_serializer(instance)
        return APIResponse(serializer.data, status=HTTPStatus.OK)
