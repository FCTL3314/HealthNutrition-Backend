from http import HTTPStatus

from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.v1.comments.models import ProductComment
from api.v1.comments.paginators import CommentPageNumberPagination
from api.v1.comments.serializers import ProductCommentSerializer


class BaseCommentModelViewSet(ModelViewSet):
    pagination_class = CommentPageNumberPagination
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=HTTPStatus.CREATED, headers=headers)


class ProductCommentModelViewSet(BaseCommentModelViewSet):
    queryset = ProductComment.objects.all()
    serializer_class = ProductCommentSerializer
