from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from api.v1.comments.models import ProductComment
from api.v1.comments.paginators import CommentPageNumberPagination
from api.v1.comments.serializers import ProductCommentSerializer
from api.v1.comments.services import ProductCommentAddService


class ProductCommentModelViewSet(ModelViewSet):
    queryset = ProductComment.objects.all()
    pagination_class = CommentPageNumberPagination
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = ProductCommentSerializer

    def create(self, request, *args, **kwargs):
        return ProductCommentAddService(
            self.serializer_class,
            request.user,
            request.data,
        ).execute()
