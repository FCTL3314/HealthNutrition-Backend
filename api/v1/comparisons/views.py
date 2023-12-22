from http import HTTPStatus

from django.db.models import QuerySet
from django.test import override_settings
from requests import Request
from rest_framework import mixins
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from api.responses import APIResponse
from api.v1.comparisons.models import Comparison, ComparisonGroup
from api.v1.comparisons.paginators import ComparisonGroupLimitOffsetPagination
from api.v1.comparisons.permissions import (
    IsComparisonGroupAuthorOrReadOnly,
    IsAuthorOfComparisonPassedInBodyIfExists,
)
from api.v1.comparisons.serializers import (
    ComparisonSerializer,
    ComparisonReadSerializer,
    ComparisonGroupReadSerializer,
    DetailedComparisonGroupSerializer,
    ComparisonGroupOrderSerializer,
)
from api.v1.comparisons.services.views import (
    ComparisonCreateService,
    ComparisonDeleteService,
)
from api.v1.products.constants import PRODUCTS_ORDERING
from api.v1.products.models import Product
from api.v1.products.paginators import (
    ProductPageLimitOffsetPagination,
)
from api.v1.products.serializers import (
    ProductWithNutritionSerializer,
)


class ComparisonGroupViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    permission_classes = (IsAuthenticated, IsComparisonGroupAuthorOrReadOnly)
    serializer_class = DetailedComparisonGroupSerializer
    pagination_class = ComparisonGroupLimitOffsetPagination
    lookup_field = "slug"

    def get_queryset(self) -> QuerySet[ComparisonGroup]:
        serializer = ComparisonGroupReadSerializer(data=self.request.query_params)
        serializer.is_valid(raise_exception=True)

        queryset = ComparisonGroup.objects.for_user(self.request.user)

        if selected_product := serializer.validated_data.get("selected_product"):
            queryset = queryset.with_is_contains_selected_product(selected_product.id)
        if serializer.validated_data.get("with_products_count") is True:
            queryset = queryset.with_products_count()
        if self.action == "retrieve":
            queryset = queryset.with_nutrition_details()

        return (
            queryset.with_unique_categories_count()
            .with_last_added_product_datetime()
            .with_standout_products()
            .position_order()
        )

    def perform_create(self, serializer) -> None:
        serializer.save(author=self.request.user)


class ComparisonGroupsChangeOrderView(APIView):
    serializer_class = ComparisonGroupOrderSerializer

    def patch(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            ComparisonGroup.objects.update_position_order(
                serializer.validated_data["ordered_ids"]
            )
            return APIResponse(status=HTTPStatus.NO_CONTENT)
        except ValueError:
            return APIResponse(
                detail="One or more provided ids do not exist in the database.",
                code="ID_DOES_NOT_EXIST",
                status=HTTPStatus.BAD_REQUEST,
            )


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
    serializer_class = ProductWithNutritionSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = ProductPageLimitOffsetPagination

    def get_queryset(self) -> QuerySet[Product]:
        queryset = Comparison.objects.products(
            self.request.query_params["comparison_group_id"]
        )
        return queryset.with_healthfulness().order_by(*PRODUCTS_ORDERING)

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
