from rest_framework.generics import ListAPIView

from api.v1.products.paginators import (
    ProductPageNumberPagination,
    ProductTypePageNumberPagination,
)
from api.v1.products.serializers import (
    ProductModelSerializer,
    ProductTypeAggregatedSerializer,
)
from api.v1.search.serializers import SearchSerializer
from api.v1.search.services import ProductSearchService, ProductTypeSearchService


class ProductTypeSearchListAPIView(ListAPIView):
    serializer_class = ProductTypeAggregatedSerializer
    pagination_class = ProductTypePageNumberPagination

    def get_queryset(self):
        search_service = ProductTypeSearchService(
            SearchSerializer, self.request.query_params
        )
        return search_service.get_searched_queryset()


class ProductSearchListAPIView(ListAPIView):
    serializer_class = ProductModelSerializer
    pagination_class = ProductPageNumberPagination

    def get_queryset(self):
        search_service = ProductSearchService(
            SearchSerializer, self.request.query_params
        )
        return search_service.get_searched_queryset()
