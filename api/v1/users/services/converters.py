from django.contrib.auth import get_user_model

from api.base.converters import IDjangoORMToDTOConverter
from api.v1.user_profiles.services.converters import UserProfileConverter
from api.v1.users.models import EmailVerification
from api.v1.users.services.schemas import EmailVerification as EmailVerificationSchema
from api.v1.users.services.schemas import User as UserSchema

User = get_user_model()


class UserConverter(IDjangoORMToDTOConverter[UserSchema]):
    def to_dto(self, user: User) -> UserSchema:
        return UserSchema(
            id=user.id,
            profile=UserProfileConverter().to_dto(user.profile),
            first_name=user.first_name,
            last_name=user.last_name,
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


class EVConverter(IDjangoORMToDTOConverter[EmailVerificationSchema]):
    def to_dto(self, email_verification: EmailVerification) -> EmailVerificationSchema:
        return EmailVerificationSchema(
            id=email_verification.id,
            code=email_verification.code,
            user_id=email_verification.user_id,
            created_at=email_verification.created_at,
            expiration=email_verification.expiration,
        )
