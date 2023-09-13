from rest_framework import mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import GenericViewSet

from api.v1.comments.docs import (
    product_comment_view_set_docs,
    store_comment_view_set_docs,
)
from api.v1.comments.filters import ProductCommentFilter, StoreCommentFilter
from api.v1.comments.models import ProductComment, StoreComment
from api.v1.comments.paginators import CommentPageNumberPagination
from api.v1.comments.serializers import ProductCommentSerializer, StoreCommentSerializer


class BaseCommentViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    pagination_class = CommentPageNumberPagination
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(edited=True)


@product_comment_view_set_docs()
class ProductCommentViewSet(BaseCommentViewSet):
    queryset = ProductComment.objects.newest()
    serializer_class = ProductCommentSerializer
    filterset_class = ProductCommentFilter


@store_comment_view_set_docs()
class StoreCommentViewSet(BaseCommentViewSet):
    queryset = StoreComment.objects.newest()
    serializer_class = StoreCommentSerializer
    filterset_class = StoreCommentFilter
