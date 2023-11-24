from django.db.models import QuerySet
from requests import Request
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.viewsets import GenericViewSet

from api.v1.comparisons.models import Comparison, ComparisonGroup
from api.v1.comparisons.permissions import (
    IsComparisonCreatorOrReadOnly,
    IsComparisonGroupAuthorOrReadOnly,
    CanCreateComparisonIfComparisonGroupAuthor,
)
from api.v1.comparisons.serializers import (
    ComparisonSerializer,
    ComparisonReadSerializer,
    ComparisonGroupSerializer,
)
from api.v1.products.constants import PRODUCTS_ORDERING
from api.v1.products.models import Product
from api.v1.products.paginators import (
    ProductPageNumberPagination,
)
from api.v1.products.serializers import (
    ProductSerializer,
)


class ComparisonGroupViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    permission_classes = (IsAuthenticated, IsComparisonGroupAuthorOrReadOnly)
    serializer_class = ComparisonGroupSerializer

    def get_queryset(self) -> QuerySet[ComparisonGroup]:
        return ComparisonGroup.objects.filter(author=self.request.user)

    def perform_create(self, serializer) -> None:
        serializer.save(author=self.request.user)


class ComparisonsViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    permission_classes = (
        IsAuthenticated,
        IsComparisonCreatorOrReadOnly,
        CanCreateComparisonIfComparisonGroupAuthor,
    )
    pagination_class = ProductPageNumberPagination

    def get_serializer_class(self) -> type[Serializer]:
        if self.action != "list":
            return ComparisonSerializer
        return ProductSerializer

    def get_queryset(self) -> QuerySet[Product]:
        queryset = Comparison.objects.all()
        if self.action != "list":
            return queryset
        queryset = queryset.products(self.request.query_params["comparison_group_id"])
        return queryset.order_by(*PRODUCTS_ORDERING)

    def list(self, request: Request, *args, **kwargs) -> Response:
        ComparisonReadSerializer(
            data=self.request.query_params,
            context=self.get_serializer_context(),
        ).is_valid(raise_exception=True)
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer: Serializer) -> None:
        serializer.save(creator=self.request.user)
