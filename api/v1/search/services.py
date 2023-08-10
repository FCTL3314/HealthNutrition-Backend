from abc import ABC, abstractmethod

from api.v1.products.models import Product, ProductType


class BaseSearchService(ABC):
    def __init__(self, request, search_serializer):
        search_serializer(data=request.query_params).is_valid(raise_exception=True)
        self.query = request.query_params.get("query")

    @abstractmethod
    def get_searched_queryset(self):
        raise NotImplementedError


class ProductTypeSearchService(BaseSearchService):
    def get_searched_queryset(self):
        searched_queryset = ProductType.objects.search(self.query)
        return searched_queryset.product_price_annotation()


class ProductSearchService(BaseSearchService):
    def get_searched_queryset(self):
        return Product.objects.search(self.query)
