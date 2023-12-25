from typing import Any

from django.contrib.auth import get_user_model
from django.db import transaction
from djoser.conf import settings

from api.v1.user_profiles.models import UserProfile

User = get_user_model()


def create_user_with_profile(data: dict[str, Any]) -> User:
    """
    Creates a user and a profile for him.
    """
    with transaction.atomic():
        profile = UserProfile.objects.create()
        user = User.objects.create_user(**data, profile=profile)
        if settings.SEND_ACTIVATION_EMAIL:
            user.is_active = False
            user.save(update_fields=["is_active"])
    return user
