from http import HTTPStatus

import pytest
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from faker import Faker

from api.utils.files import mb_to_bytes
from api.utils.tests import is_objects_fields_match, generate_test_image
from api.v1.user_profiles.constants import (
    MAX_USER_BODY_WEIGHT_KG,
    MIN_USER_BODY_WEIGHT_KG,
    MAX_USER_IMAGE_SIZE_MB,
)
from api.v1.user_profiles.serializers import UserProfileSerializer
from api.v1.user_profiles.services.infrastructure.user_profile_update import (
    UserProfileUpdateService,
)

User = get_user_model()


class TestUserProfileUpdateService:
    @pytest.mark.django_db
    def test_update(self, user: User, faker: Faker):
        data = {
            "about": faker.text(),
            "body_weight": faker.pyfloat(
                min_value=MIN_USER_BODY_WEIGHT_KG, max_value=MAX_USER_BODY_WEIGHT_KG
            ),
        }
        profile = user.profile
        response = UserProfileUpdateService(
            profile,
            UserProfileSerializer,
            data,
            True,
        ).execute()

        profile.refresh_from_db()
        assert response.status_code == HTTPStatus.OK
        assert is_objects_fields_match(response.data, profile, ("about", "body_weight"))

    @pytest.mark.django_db
    def test_valid_image_size(self, user: User):
        profile = user.profile
        old_image = profile.image
        response = UserProfileUpdateService(
            user,
            UserProfileSerializer,
            {"image": generate_test_image()},
            True,
        ).execute()

        profile.refresh_from_db()
        assert response.status_code == HTTPStatus.OK
        assert old_image != profile.image

    @pytest.mark.django_db
    def test_invalid_image_size(self, user: User):
        response = UserProfileUpdateService(
            user,
            UserProfileSerializer,
            {"image": self._image_with_invalid_size},
            True,
        ).execute()

        assert response.status_code == HTTPStatus.REQUEST_ENTITY_TOO_LARGE
        user.profile.refresh_from_db()
        assert not user.profile.image

    @property
    def _image_with_invalid_size(self) -> SimpleUploadedFile:
        image = generate_test_image()
        image.size = mb_to_bytes(MAX_USER_IMAGE_SIZE_MB * 2)
        return image


if __name__ == "__main__":
    pytest.main()
