from dataclasses import dataclass
from datetime import datetime

from django.contrib.auth import get_user_model

from api.common.adapters import BaseORMToDTOAdapter

User = get_user_model()


@dataclass
class UserDTO:
    id: int
    image: str
    first_name: str
    last_name: str
    about: str
    username: str
    slug: str
    email: str
    password: str
    is_superuser: bool
    is_staff: bool
    is_active: bool
    is_verified: bool
    date_joined: datetime
    last_login: datetime


class UserAdapter(BaseORMToDTOAdapter[UserDTO]):
    dto_class = UserDTO
    fields = (
        "id",
        "image",
        "first_name",
        "last_name",
        "about",
        "username",
        "slug",
        "email",
        "password",
        "is_superuser",
        "is_staff",
        "is_active",
        "is_verified",
        "date_joined",
        "last_login",
    )


@dataclass
class EmailVerificationDTO:
    id: int
    code: str
    user_id: int
    created_at: datetime
    expiration: datetime


class EVAdapter(BaseORMToDTOAdapter[EmailVerificationDTO]):
    dto_class = EmailVerificationDTO
    fields = (
        "id",
        "code",
        "user_id",
        "created_at",
        "expiration",
    )
