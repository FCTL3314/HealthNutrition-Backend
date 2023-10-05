from django.core.files.uploadedfile import SimpleUploadedFile, TemporaryUploadedFile
from django.utils.timezone import now
from faker import Faker
from rest_framework_simplejwt.tokens import AccessToken

from api.v1.users.constants import EV_EXPIRATION_TIMEDELTA
from api.v1.users.models import User


def generate_test_image() -> SimpleUploadedFile:
    """Returns a representation of an image file."""
    return SimpleUploadedFile(
        "test_generated_image.jpg", Faker().image(), content_type="image/jpg"
    )


def generate_temporary_image(size: int = 1000) -> TemporaryUploadedFile:
    """Returns a representation of an temporary image file."""
    return TemporaryUploadedFile(
        "test_generated_image.jpg",
        Faker().image(),
        size=size,
        charset=None,
    )


def get_access_token(user: User) -> AccessToken:
    """Return an access token for provided user."""
    return AccessToken.for_user(user)


def get_auth_header(user: User) -> dict[str, str]:
    """Returns an authorization header based on received token."""
    token = get_access_token(user)
    return {"HTTP_AUTHORIZATION": f"Bearer {token}"}


def get_expired_email_verification_kwargs() -> dict:
    return {"expiration": now() - EV_EXPIRATION_TIMEDELTA}
