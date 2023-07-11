from django.core.files.uploadedfile import SimpleUploadedFile
from faker import Faker
from rest_framework_simplejwt.tokens import AccessToken, Token

faker = Faker()


def generate_test_image() -> SimpleUploadedFile:
    """Returns a representation of an image file."""
    return SimpleUploadedFile(
        "test_generated_image.jpg", faker.image(), content_type="image/jpg"
    )


def get_access_token(user) -> AccessToken:
    return AccessToken.for_user(user)


def get_authorization_header(token: Token) -> dict:
    return {
        "HTTP_AUTHORIZATION": f"Bearer {token}"
    }
