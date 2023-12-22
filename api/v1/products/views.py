from http import HTTPStatus
from typing import Any

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.viewsets import ModelViewSet

from api.common.filters import TrigramSimilaritySearchFilter
from api.common.permissions import IsAdminOrReadOnly
from api.utils.network import get_client_address
from api.v1.products.constants import PRODUCTS_ORDERING
from api.v1.products.filters import ProductFilter
from api.v1.products.models import Product
from api.v1.products.paginators import (
    ProductPageNumberPagination,
)
from api.v1.products.serializers import (
    ProductWithNutritionSerializer,
    DetailedProductSerializer,
    ProductReadSerializer,
)
from api.v1.products.services import (
    ProductViewsIncreaseService,
)


class ProductViewSet(ModelViewSet):
    queryset = (
        Product.objects.select_related("nutrition", "category")
        .with_healthfulness()
        .order_by(*PRODUCTS_ORDERING)
    )
    filterset_class = ProductFilter
    filter_backends = (
        DjangoFilterBackend,
        TrigramSimilaritySearchFilter,
    )
    search_fields = ("name", "short_description")
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = ProductPageNumberPagination
    lookup_field = "slug"

    def get_serializer_class(self) -> type[Serializer]:
        if self.action == "retrieve":
            return DetailedProductSerializer
        return ProductWithNutritionSerializer

    def get_serializer_context(self) -> dict[str, Any]:
        context = super().get_serializer_context()
        request = context["request"]
        context["body_weight"] = request.query_params.get("body_weight")
        return context

    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        ProductReadSerializer(data=self.request.query_params).is_valid(
            raise_exception=True
        )
        instance = self.get_object()
        ProductViewsIncreaseService(instance, get_client_address(request)).execute()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=HTTPStatus.OK)
