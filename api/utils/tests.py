from datetime import datetime
from typing import Any, Iterable

from django.core.files.uploadedfile import SimpleUploadedFile
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


def get_auth_header(user: User) -> dict[str, str]:
    """Returns an authorization header based on received token."""
    token = AccessToken.for_user(user)
    return {"HTTP_AUTHORIZATION": f"Bearer {token}"}


def get_expired_email_verification_kwarg() -> dict[str, datetime]:
    return {"expiration": now() - EV_EXPIRATION_TIMEDELTA}


def is_objects_fields_match(
    first_object: dict | object, second_object: dict | object, fields: Iterable[str]
) -> bool:
    """
    Checks whether the fields of the first object
    are equal to the fields of the second object.
    """

    def get_field(obj, key: str) -> Any:
        try:
            return obj[key] if isinstance(obj, dict) else getattr(obj, key)
        except KeyError:
            raise ValueError(
                f"One of the provided objects is missing the '{key}' field."
            )

    for field in fields:
        first_object_field = get_field(first_object, field)
        second_object_field = get_field(second_object, field)
        if first_object_field != second_object_field:
            return False
    return True
