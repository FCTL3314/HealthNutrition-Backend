from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from api.v1.comparisons.models import ComparisonGroup, Comparison


class IsComparisonGroupAuthorOrReadOnly(BasePermission):
    def has_object_permission(
        self, request: Request, view: APIView, comparison_group: ComparisonGroup
    ) -> bool:
        return bool(
            request.method in SAFE_METHODS or request.user == comparison_group.author
        )


class IsComparisonCreatorOrReadOnly(BasePermission):
    def has_object_permission(
        self, request: Request, view: APIView, comparison: Comparison
    ) -> bool:
        return bool(
            request.method in SAFE_METHODS or request.user == comparison.creator
        )


class IsAuthorOfComparisonPassedInBodyIfExists(BasePermission):
    def has_permission(self, request: Request, view: GenericViewSet) -> bool:
        try:
            comparison_group = ComparisonGroup.objects.get(
                id=request.data["comparison_group_id"]
            )
            return bool(
                request.method in SAFE_METHODS
                or request.user == comparison_group.author
            )
        except (KeyError, ComparisonGroup.DoesNotExist):
            return True
