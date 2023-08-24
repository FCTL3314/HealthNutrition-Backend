from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from api.v1.comments.models import ProductComment, StoreComment
from api.v1.comments.paginators import CommentPageNumberPagination
from api.v1.comments.serializers import ProductCommentSerializer, StoreCommentSerializer


class BaseCommentViewSet(ModelViewSet):
    pagination_class = CommentPageNumberPagination
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(edited=True)


class ProductCommentViewSet(BaseCommentViewSet):
    queryset = ProductComment.objects.all()
    serializer_class = ProductCommentSerializer


class StoreCommentViewSet(BaseCommentViewSet):
    queryset = StoreComment.objects.all()
    serializer_class = StoreCommentSerializer
