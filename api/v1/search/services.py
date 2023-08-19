from abc import ABC, abstractmethod

from rest_framework.serializers import Serializer

from api.v1.products.models import Product, ProductType


class ISearchService(ABC):
    def __init__(self, serializer_class: type[Serializer], data: dict):
        serializer_class(data=data).is_valid(raise_exception=True)
        self.query = data.get("query")

    @abstractmethod
    def get_searched_queryset(self):
        ...


class ProductTypeSearchService(ISearchService):
    def get_searched_queryset(self):
        searched_queryset = ProductType.objects.search(self.query)
        return searched_queryset.products_price_annotation()


class ProductSearchService(ISearchService):
    def get_searched_queryset(self):
        return Product.objects.search(self.query)
