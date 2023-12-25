from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from api.v1.user_profiles.constants import (
    DEFAULT_USER_BODY_WEIGHT_KG,
    MAX_USER_BODY_WEIGHT_KG,
    MIN_USER_BODY_WEIGHT_KG,
)


class UserProfile(models.Model):
    image = models.ImageField(upload_to="users", null=True, blank=True)
    about = models.TextField(max_length=516, null=True, blank=True)
    body_weight = models.FloatField(
        default=DEFAULT_USER_BODY_WEIGHT_KG,
        validators=(
            MaxValueValidator(MAX_USER_BODY_WEIGHT_KG),
            MinValueValidator(MIN_USER_BODY_WEIGHT_KG),
        ),
    )

    def __str__(self):
        return f"{self.user.username}'s profile"
