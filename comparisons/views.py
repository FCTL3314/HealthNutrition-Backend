from django.conf import settings
from rest_framework.generics import ListAPIView
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from common.decorators import order_queryset
from comparisons.serializers import ComparisonModelSerializer
from comparisons.services import ComparisonModifyService, ComparisonListService
from products.paginators import (
    ProductPageNumberPagination,
    ProductTypePageNumberPagination,
)
from products.serializers import ProductModelSerializer, ProductTypeAggregatedSerializer


class ComparisonGenericViewSet(GenericViewSet, CreateModelMixin, DestroyModelMixin):
    permission_classes = (IsAuthenticated,)
    serializer_class = ComparisonModelSerializer

    @property
    def comparison_modify_service(self):
        return ComparisonModifyService(self.kwargs["product_id"])

    def create(self, request, *args, **kwargs):
        return self.comparison_modify_service.add(request.user, self.serializer_class)

    def destroy(self, request, *args, **kwargs):
        return self.comparison_modify_service.remove(request.user)


class ComparedProductTypesListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductTypeAggregatedSerializer
    pagination_class = ProductTypePageNumberPagination
    ordering = settings.PRODUCT_TYPES_ORDERING

    @order_queryset(*ordering)
    def get_queryset(self):
        return ComparisonListService(self.request.user).product_types_list()


class ComparedProductsListApiView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductModelSerializer
    pagination_class = ProductPageNumberPagination
    ordering = settings.PRODUCTS_ORDERING

    @order_queryset(*ordering)
    def get_queryset(self):
        return ComparisonListService(self.request.user).products_list(
            self.kwargs["slug"]
        )
