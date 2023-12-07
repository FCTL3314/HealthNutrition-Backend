from rest_framework.pagination import LimitOffsetPagination

from api.v1.comparisons.constants import (
    COMPARISON_GROUPS_DEFAULT_PAGINATION_LIMIT,
    COMPARISON_GROUPS_MAX_PAGINATION_LIMIT,
)


class ComparisonGroupLimitOffsetPagination(LimitOffsetPagination):
    default_limit = COMPARISON_GROUPS_DEFAULT_PAGINATION_LIMIT
    max_limit = COMPARISON_GROUPS_MAX_PAGINATION_LIMIT
