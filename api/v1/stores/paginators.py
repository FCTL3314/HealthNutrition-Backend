from django.conf import settings
from rest_framework.pagination import PageNumberPagination


class StorePageNumberPagination(PageNumberPagination):
    page_size = settings.STORES_PAGINATE_BY
