from django.db.models import QuerySet
from django.test import override_settings
from requests import Request
from rest_framework import mixins
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.responses import APIResponse
from api.v1.comparisons.models import Comparison, ComparisonGroup
from api.v1.comparisons.paginators import ComparisonGroupPageNumberPagination
from api.v1.comparisons.permissions import (
    IsComparisonGroupAuthorOrReadOnly,
    IsAuthorOfComparisonPassedInBodyIfExists,
)
from api.v1.comparisons.serializers import (
    ComparisonSerializer,
    ComparisonReadSerializer,
    ComparisonGroupSerializer,
)
from api.v1.comparisons.services import ComparisonCreateService, ComparisonDeleteService
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
    pagination_class = ComparisonGroupPageNumberPagination

    def get_queryset(self) -> QuerySet[ComparisonGroup]:
        queryset = ComparisonGroup.objects.newest()
        if selected_product_id := self.request.query_params.get("selected_product_id"):
            queryset = queryset.with_is_contains_selected_product(selected_product_id)
        return queryset.filter(author=self.request.user)

    def perform_create(self, serializer) -> None:
        serializer.save(author=self.request.user)


class ComparisonCreateView(CreateAPIView):
    queryset = Comparison.objects.all()
    serializer_class = ComparisonSerializer
    permission_classes = (
        IsAuthenticated,
        IsAuthorOfComparisonPassedInBodyIfExists,
    )

    def create(self, request: Request, *args, **kwargs) -> Response | APIResponse:
        return ComparisonCreateService(
            self.get_serializer_class(), self.request.data, self.request.user
        ).execute()


class ComparisonListView(ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = ProductPageNumberPagination

    def get_queryset(self) -> QuerySet[Product]:
        queryset = Comparison.objects.products(
            self.request.query_params["comparison_group_id"]
        )
        return queryset.order_by(*PRODUCTS_ORDERING)

    @override_settings(CACHEOPS_ENABLED=False)
    def list(self, request: Request, *args, **kwargs) -> Response:
        ComparisonReadSerializer(
            data=self.request.query_params,
            context=self.get_serializer_context(),
        ).is_valid(raise_exception=True)
        return super().list(request, *args, **kwargs)


class ComparisonsDestroyView(DestroyAPIView):
    queryset = Comparison.objects.all()
    serializer_class = ComparisonSerializer
    permission_classes = (
        IsAuthenticated,
        IsAuthorOfComparisonPassedInBodyIfExists,
    )

    def destroy(self, request: Request, *args, **kwargs) -> Response:
        return ComparisonDeleteService(
            self.get_serializer_class(), self.request.data
        ).execute()
