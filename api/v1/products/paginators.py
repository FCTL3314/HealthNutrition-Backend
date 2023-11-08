from rest_framework.pagination import PageNumberPagination

from api.v1.products.constants import PRODUCTS_PAGINATE_BY


class ProductPageNumberPagination(PageNumberPagination):
    page_size = PRODUCTS_PAGINATE_BY
