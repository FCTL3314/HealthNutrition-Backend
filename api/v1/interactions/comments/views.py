from django.db.models import Model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.v1.interactions.comments.serializers import StoreCommentModelSerializer, ProductCommentModelSerializer
from interactions.comments.models import StoreComment, ProductComment
from products.models import Product
from stores.models import Store


class BaseCommentCreateAPIView(CreateAPIView):
    comment_model: Model = None
    related_model: Model = None
    identifier_field: str = "slug"
    identifier_kwarg: str = "slug"
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        self.get_serializer(data=request.data).is_valid(raise_exception=True)
        text = request.data["text"]
        comment = self._create_comment(text=text)
        serializer = self.get_serializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def _create_comment(self, text: str):
        comment_data = {
            "text": text,
            "author": self.request.user,
            self.related_model._meta.model_name: self._get_related_object(),
        }
        return self.comment_model.objects.create(**comment_data)

    def _get_identifier(self):
        return self.request.data[self.identifier_kwarg]

    def _get_related_object(self):
        kwargs = {self.identifier_field: self._get_identifier()}
        return get_object_or_404(self.related_model, **kwargs)


class StoreCommentCreateAPIView(BaseCommentCreateAPIView):
    comment_model = StoreComment
    related_model = Store
    identifier_field = "slug"
    identifier_kwarg = "store_slug"
    serializer_class = StoreCommentModelSerializer


class ProductCommentCreateAPIView(BaseCommentCreateAPIView):
    comment_model = ProductComment
    related_model = Product
    identifier_field = "slug"
    identifier_kwarg = "product_slug"
    serializer_class = ProductCommentModelSerializer
