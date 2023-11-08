from rest_framework.pagination import PageNumberPagination

from api.v1.categories.constants import CATEGORIES_PAGINATE_BY


class CategoryPageNumberPagination(PageNumberPagination):
    page_size = CATEGORIES_PAGINATE_BY
