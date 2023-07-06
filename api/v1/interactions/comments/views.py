from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.v1.interactions.comments.serializers import (
    ProductCommentModelSerializer, StoreCommentModelSerializer)
from interactions.comments.mixins import CommentCreateMixin
from interactions.comments.models import ProductComment, StoreComment
from products.models import Product
from stores.models import Store


class BaseCommentCreateAPIView(CommentCreateMixin, CreateAPIView):
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        self.get_serializer(data=request.data).is_valid(raise_exception=True)
        text = request.data["text"]
        comment = self.create_comment(text=text, author=request.user)
        serializer = self.get_serializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_identifier(self):
        return self.request.data[self.identifier_kwarg]


class StoreCommentCreateAPIView(BaseCommentCreateAPIView):
    comment_model = StoreComment
    related_model = Store
    identifier_kwarg = "store_slug"
    serializer_class = StoreCommentModelSerializer


class ProductCommentCreateAPIView(BaseCommentCreateAPIView):
    comment_model = ProductComment
    related_model = Product
    identifier_kwarg = "product_slug"
    serializer_class = ProductCommentModelSerializer
