from dataclasses import dataclass
from datetime import datetime

from django.contrib.auth import get_user_model

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

    @staticmethod
    def to_dto(user) -> "UserDTO":
        return UserDTO(
            id=user.id,
            image=user.image,
            first_name=user.first_name,
            last_name=user.last_name,
            about=user.about,
            username=user.username,
            slug=user.slug,
            email=user.email,
            password=user.password,
            is_superuser=user.is_superuser,
            is_staff=user.is_staff,
            is_active=user.is_active,
            is_verified=user.is_verified,
            date_joined=user.date_joined,
            last_login=user.last_login,
        )


@dataclass
class EmailVerificationDTO:
    id: int
    code: str
    user_id: int
    created_at: datetime
    expiration: datetime

    @staticmethod
    def to_dto(verification) -> "EmailVerificationDTO":
        return EmailVerificationDTO(
            id=verification.id,
            code=verification.code,
            user_id=verification.user_id,
            created_at=verification.created_at,
            expiration=verification.expiration,
        )
