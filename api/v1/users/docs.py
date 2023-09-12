from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from rest_framework import status

from api.v1.users.serializers import CurrentUserSerializer, EmailVerificationSerializer

EMAIL_VERIFICATION_VIEW_RESPONSES = {
    status.HTTP_201_CREATED: OpenApiResponse(
        response=EmailVerificationSerializer,
        description=(
            "The email verification email was successfully " "sent to the user's email."
        ),
    ),
    status.HTTP_429_TOO_MANY_REQUESTS: OpenApiResponse(
        description="The time limit for sending emails has been " "reached.",
    ),
    status.HTTP_400_BAD_REQUEST: OpenApiResponse(
        description="The user's email has already been verified.",
    ),
}


def email_verification_view_docs() -> callable(extend_schema_view):
    return extend_schema_view(
        post=extend_schema(
            summary="Sends an email verification letter.",
            request=None,
            responses=EMAIL_VERIFICATION_VIEW_RESPONSES,
        ),
    )


VERIFY_EMAIL_VIEW_RESPONSES = {
    status.HTTP_200_OK: OpenApiResponse(
        response=CurrentUserSerializer,
        description="The user's email has been successfully " "verified.",
    ),
    status.HTTP_410_GONE: OpenApiResponse(
        description="The verification code has expired.",
    ),
    status.HTTP_400_BAD_REQUEST: OpenApiResponse(
        description="Invalid verification code.",
    ),
}


def verify_email_view_docs() -> callable(extend_schema_view):
    return extend_schema_view(
        post=extend_schema(
            summary="Confirms the user's email if the code is correct.",
            responses=VERIFY_EMAIL_VIEW_RESPONSES,
        ),
    )
