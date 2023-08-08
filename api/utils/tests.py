from django.core.files.uploadedfile import SimpleUploadedFile
from faker import Faker
from rest_framework_simplejwt.tokens import AccessToken, Token

from api.v1.users.models import User


def generate_test_image() -> SimpleUploadedFile:
    """Returns a representation of an image file."""
    return SimpleUploadedFile(
        "test_generated_image.jpg", Faker().image(), content_type="image/jpg"
    )


def get_access_token(user: User) -> AccessToken:
    """Return an access token for provided user."""
    return AccessToken.for_user(user)


def get_authorization_header(token: Token) -> dict[str, str]:
    """Returns an authorization header based on received token."""
    return {"HTTP_AUTHORIZATION": f"Bearer {token}"}
