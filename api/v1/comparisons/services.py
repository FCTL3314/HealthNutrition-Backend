from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.serializers import Serializer

from api.common.services import AbstractService
from api.responses import APIResponse
from api.v1.comparisons.models import Comparison
from api.v1.products.models import Product

User = get_user_model()


class ComparisonAddService(AbstractService):
    def __init__(self, serializer: type[Serializer], user: User, product_id: int):
        self._serializer = serializer
        self._user = user
        self._product = get_object_or_404(Product, pk=product_id)

    def execute(self) -> APIResponse:
        comparison = Comparison.objects.create(user=self._user, product=self._product)
        return APIResponse(
            self._serializer(comparison).data,
            status=status.HTTP_201_CREATED,
        )


class ComparisonRemoveService(AbstractService):
    def __init__(self, user: User, product_id: int):
        self._user = user
        self._product = get_object_or_404(Product, pk=product_id)

    def execute(self) -> APIResponse:
        self._user.comparisons.remove(self._product)
        return APIResponse(status=status.HTTP_204_NO_CONTENT)
