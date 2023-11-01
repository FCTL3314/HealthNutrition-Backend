from django.db.models import QuerySet
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.serializers import Serializer
from rest_framework.viewsets import GenericViewSet

from api.v1.comments.filters import CommentFilter
from api.v1.comments.models import Comment
from api.v1.comments.paginators import CommentPageNumberPagination
from api.v1.comments.serializers import CommentSerializer


class CommentViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    model = Comment
    serializer_class = CommentSerializer
    pagination_class = CommentPageNumberPagination
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filterset_class = CommentFilter
    filterset_actions = ("list",)

    def filter_queryset(self, queryset):
        """
        A wrapper that allows queryset filtering
        only if the query is sent by the correct
        method.
        """
        if self.action in self.filterset_actions:
            return super().filter_queryset(queryset)
        return queryset

    def get_queryset(self) -> QuerySet[Comment]:
        queryset = self.model.objects.newest()
        if self.action != "list":
            return queryset
        if parent_id := self.request.query_params.get("parent_id"):
            return queryset.filter(parent_id=parent_id)
        return queryset.top_level()

    def perform_create(self, serializer: Serializer) -> None:
        serializer.save(author=self.request.user)

    def perform_update(self, serializer: Serializer) -> None:
        serializer.save(edited=True)
