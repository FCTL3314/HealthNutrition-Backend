from rest_framework.generics import ListAPIView
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from api.v1.comparisons.serializers import ComparisonModelSerializer
from api.v1.comparisons.services import ComparisonModifyService, ComparisonListService
from api.v1.products.paginators import (
    ProductPageNumberPagination,
    ProductTypePageNumberPagination,
)
from api.v1.products.serializers import (
    ProductModelSerializer,
    ProductTypeAggregatedSerializer,
)


class ComparisonGenericViewSet(GenericViewSet, CreateModelMixin, DestroyModelMixin):
    permission_classes = (IsAuthenticated,)
    serializer_class = ComparisonModelSerializer

    @property
    def comparison_modify_service(self):
        return ComparisonModifyService(
            self.kwargs["product_id"],
            self.request.user,
            self.serializer_class,
        )

    def create(self, request, *args, **kwargs):
        return self.comparison_modify_service.add()

    def destroy(self, request, *args, **kwargs):
        return self.comparison_modify_service.remove()


class ComparedProductTypesListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductTypeAggregatedSerializer
    pagination_class = ProductTypePageNumberPagination

    def get_queryset(self):
        return ComparisonListService(self.request.user).product_types_list()


class ComparedProductsListApiView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductModelSerializer
    pagination_class = ProductPageNumberPagination

    def get_queryset(self):
        return ComparisonListService(self.request.user).products_list(
            self.kwargs["slug"]
        )
