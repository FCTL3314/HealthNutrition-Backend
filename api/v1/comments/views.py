import django_filters
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.serializers import Serializer
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
    _filterset_class = None
    filterset_actions = ("list",)

    def perform_create(self, serializer: Serializer) -> None:
        serializer.save(author=self.request.user)

    def perform_update(self, serializer: Serializer) -> None:
        serializer.save(edited=True)

    @property
    def is_filterset_action(self) -> bool:
        return self.action in self.filterset_actions

    @property
    def filterset_class(self) -> type[django_filters.FilterSet] | None:
        if self.is_filterset_action:
            return self._filterset_class
        return None


@product_comment_view_set_docs()
class ProductCommentViewSet(BaseCommentViewSet):
    queryset = ProductComment.objects.newest()
    serializer_class = ProductCommentSerializer
    _filterset_class = ProductCommentFilter


@store_comment_view_set_docs()
class StoreCommentViewSet(BaseCommentViewSet):
    queryset = StoreComment.objects.newest()
    serializer_class = StoreCommentSerializer
    _filterset_class = StoreCommentFilter
