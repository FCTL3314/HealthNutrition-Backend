from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from api.v1.comments.models import ProductComment
from api.v1.comments.paginators import CommentPageNumberPagination
from api.v1.comments.serializers import ProductCommentSerializer
from api.v1.comments.services import CommentService


class ProductCommentModelViewSet(ModelViewSet):
    queryset = ProductComment.objects.all()
    pagination_class = CommentPageNumberPagination
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = ProductCommentSerializer

    def create(self, request, *args, **kwargs):
        comment_service = CommentService(self.serializer_class, request)
        return comment_service.create()
