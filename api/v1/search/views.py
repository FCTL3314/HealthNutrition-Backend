from rest_framework.generics import ListAPIView

from api.v1.products.paginators import ProductTypePageNumberPagination
from api.v1.products.serializers import ProductTypeAggregatedSerializer
from api.v1.search.serializers import SearchSerializer
from api.v1.search.services import ProductSearchService


class ProductTypeSearchListAPIView(ListAPIView):
    serializer_class = ProductTypeAggregatedSerializer
    pagination_class = ProductTypePageNumberPagination

    def get_queryset(self):
        search_service = ProductSearchService(self.request, SearchSerializer)
        return search_service.get_searched_queryset()
