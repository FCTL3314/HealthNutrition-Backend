from rest_framework.pagination import PageNumberPagination

from api.v1.comparisons.constants import COMPARISON_GROUPS_PAGINATE_BY


class ComparisonGroupPageNumberPagination(PageNumberPagination):
    page_size = COMPARISON_GROUPS_PAGINATE_BY
