from rest_framework.pagination import PageNumberPagination

from api.v1.products.constraints import (PRODUCT_TYPES_PAGINATE_BY,
                                         PRODUCTS_PAGINATE_BY)


class ProductTypePageNumberPagination(PageNumberPagination):
    page_size = PRODUCT_TYPES_PAGINATE_BY


class ProductPageNumberPagination(PageNumberPagination):
    page_size = PRODUCTS_PAGINATE_BY
