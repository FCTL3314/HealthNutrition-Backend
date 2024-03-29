from rest_framework.pagination import PageNumberPagination

from api.v1.comments.constants import COMMENTS_PAGINATE_BY


class CommentPageNumberPagination(PageNumberPagination):
    page_size = COMMENTS_PAGINATE_BY
