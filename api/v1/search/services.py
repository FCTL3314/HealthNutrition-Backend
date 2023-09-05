from abc import ABC, abstractmethod

from django.db.models import QuerySet
from rest_framework.serializers import Serializer

from api.decorators import order_queryset
from api.v1.products.constants import PRODUCT_TYPES_ORDERING, PRODUCTS_ORDERING
from api.v1.products.models import Product, ProductType


class ISearchService(ABC):
    @abstractmethod
    def get_searched_queryset(self):
        ...


class BaseSearchService(ISearchService, ABC):
    def __init__(self, serializer_class: type[Serializer], data: dict):
        serializer_class(data=data).is_valid(raise_exception=True)
        self.query = data.get("query")


class ProductTypeSearchService(BaseSearchService):
    @order_queryset(*PRODUCT_TYPES_ORDERING)
    def get_searched_queryset(self) -> QuerySet[ProductType]:
        searched_queryset = ProductType.objects.search(self.query)
        return searched_queryset.products_annotation()


class ProductSearchService(BaseSearchService):
    @order_queryset(*PRODUCTS_ORDERING)
    def get_searched_queryset(self) -> QuerySet[Product]:
        return Product.objects.search(self.query)
