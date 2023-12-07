from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination

from api.v1.products.constants import PRODUCTS_PAGINATE_BY


class ProductPageNumberPagination(PageNumberPagination):
    page_size = PRODUCTS_PAGINATE_BY


class ProductPageLimitOffsetPagination(LimitOffsetPagination):
    default_limit = PRODUCTS_PAGINATE_BY
