from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from rest_framework import status

from api.v1.comparisons.serializers import ComparisonSerializer

COMPARISON_CREATE_VIEW_RESPONSES = {
    status.HTTP_201_CREATED: OpenApiResponse(
        response=ComparisonSerializer,
        description=(
            "The product has been successfully added to the user's comparisons."
        ),
    ),
}


def comparison_create_view_docs():
    return extend_schema_view(
        post=extend_schema(
            summary="Adds a product to the user's comparisons.",
            request=None,
            responses=COMPARISON_CREATE_VIEW_RESPONSES,
        ),
    )


COMPARISON_DELETE_VIEW_RESPONSES = {
    status.HTTP_204_NO_CONTENT: OpenApiResponse(
        description="The product has been successfully deleted from the user's comparisons.",
    ),
}


def comparison_delete_view_docs():
    return extend_schema_view(
        delete=extend_schema(
            summary="Deletes a product from the user's comparisons.",
            responses=COMPARISON_DELETE_VIEW_RESPONSES,
        )
    )
