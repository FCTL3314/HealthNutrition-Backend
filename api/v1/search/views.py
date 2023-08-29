from rest_framework.generics import ListAPIView

from api.v1.products.paginators import (
    ProductPageNumberPagination,
    ProductTypePageNumberPagination,
)
from api.v1.products.serializers import (
    ProductSerializer,
    ProductTypeAggregatedSerializer,
)
from api.v1.search.serializers import SearchSerializer
from api.v1.search.services import ProductSearchService, ProductTypeSearchService


class ProductTypeSearchListView(ListAPIView):
    serializer_class = ProductTypeAggregatedSerializer
    pagination_class = ProductTypePageNumberPagination

    def get_queryset(self):
        return ProductTypeSearchService(
            SearchSerializer, self.request.query_params
        ).get_searched_queryset()


class ProductSearchListView(ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = ProductPageNumberPagination

    def get_queryset(self):
        return ProductSearchService(
            SearchSerializer, self.request.query_params
        ).get_searched_queryset()
