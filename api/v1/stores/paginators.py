from rest_framework.pagination import PageNumberPagination

from api.v1.stores.constants import STORES_PAGINATE_BY


class StorePageNumberPagination(PageNumberPagination):
    page_size = STORES_PAGINATE_BY
