from django.conf import settings
from rest_framework.pagination import PageNumberPagination


class ProductTypePageNumberPagination(PageNumberPagination):
    page_size = settings.PRODUCT_TYPES_PAGINATE_BY


class ProductPageNumberPagination(PageNumberPagination):
    page_size = settings.PRODUCTS_PAGINATE_BY
