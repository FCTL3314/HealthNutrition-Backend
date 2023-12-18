from http import HTTPStatus

from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet

from api.common.permissions import IsAdminOrReadOnly
from api.filters import TrigramSimilaritySearchFilter
from api.responses import APIResponse
from api.utils.network import get_client_address
from api.v1.categories.constants import CATEGORIES_ORDERING
from api.v1.categories.models import Category
from api.v1.categories.paginators import CategoryPageNumberPagination
from api.v1.categories.serializers import DetailedCategorySerializer
from api.v1.categories.services import (
    CategoryViewsIncreaseService,
)


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.with_nutrition_averages_details().order_by(
        *CATEGORIES_ORDERING
    )
    filter_backends = (TrigramSimilaritySearchFilter,)
    search_fields = ("name", "description")
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = DetailedCategorySerializer
    pagination_class = CategoryPageNumberPagination
    lookup_field = "slug"

    def retrieve(self, request: Request, *args, **kwargs) -> APIResponse:
        instance = self.get_object()
        CategoryViewsIncreaseService(instance, get_client_address(request)).execute()
        serializer = self.get_serializer(instance)
        return APIResponse(serializer.data, status=HTTPStatus.OK)
