from rest_framework.pagination import LimitOffsetPagination

from api.v1.comparisons.constants import (
    COMPARISON_GROUPS_PAGINATE_BY,
)


class ComparisonGroupLimitOffsetPagination(LimitOffsetPagination):
    default_limit = COMPARISON_GROUPS_PAGINATE_BY
