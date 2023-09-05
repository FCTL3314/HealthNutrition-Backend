from rest_framework.pagination import PageNumberPagination

from api.v1.users.constants import USERS_PAGINATE_BY


class UserPageNumberPagination(PageNumberPagination):
    page_size = USERS_PAGINATE_BY
