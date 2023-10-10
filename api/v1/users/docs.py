from http import HTTPStatus

from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view

from api.v1.users.serializers import CurrentUserSerializer, EmailVerificationSerializer

USER_CHANGE_EMAIL_VIEW_RESPONSES = {
    HTTPStatus.OK: OpenApiResponse(
        description="The user's email address has been successfully changed.",
        response=CurrentUserSerializer,
    ),
    HTTPStatus.BAD_REQUEST: OpenApiResponse(
        description="The new email is the same as the old one.",
    ),
}


def user_send_email_verification_view_docs() -> callable(extend_schema_view):
    return extend_schema_view(
        post=extend_schema(
            summary="Changes the user's email to a new one.",
            responses=USER_CHANGE_EMAIL_VIEW_RESPONSES,
        ),
    )


USER_SEND_EMAIL_VERIFICATION_VIEW_RESPONSES = {
    HTTPStatus.CREATED: OpenApiResponse(
        description=(
            "The email verification email was successfully sent to the user's email."
        ),
        response=EmailVerificationSerializer,
    ),
    HTTPStatus.TOO_MANY_REQUESTS: OpenApiResponse(
        description="The time limit for sending emails has been reached.",
    ),
    HTTPStatus.BAD_REQUEST: OpenApiResponse(
        description="The user's email has already been verified.",
    ),
}


def user_change_email_view_docs() -> callable(extend_schema_view):
    return extend_schema_view(
        post=extend_schema(
            summary="Sends an email verification letter.",
            request=None,
            responses=USER_SEND_EMAIL_VERIFICATION_VIEW_RESPONSES,
        ),
    )


USER_EMAIL_VERIFIER_VIEW_RESPONSES = {
    HTTPStatus.OK: OpenApiResponse(
        description="The user's email has been successfully verified.",
        response=CurrentUserSerializer,
    ),
    HTTPStatus.GONE: OpenApiResponse(
        description="The verification code has expired.",
    ),
    HTTPStatus.BAD_REQUEST: OpenApiResponse(
        description="Invalid verification code.",
    ),
}


def user_email_verifier_view_docs() -> callable(extend_schema_view):
    return extend_schema_view(
        post=extend_schema(
            summary="Confirms the user's email if the code is correct.",
            responses=USER_EMAIL_VERIFIER_VIEW_RESPONSES,
        ),
    )
