from api.base.converters import IDjangoORMToDTOConverter
from api.v1.user_profiles.models import UserProfile
from api.v1.user_profiles.services.schemas import (
    UserProfile as UserProfileSchema,
)


class UserProfileConverter(IDjangoORMToDTOConverter[UserProfileSchema]):
    def to_dto(self, user_profile: UserProfile) -> UserProfileSchema:
        return UserProfileSchema(
            id=user_profile.id,
            image=user_profile.image.url if user_profile.image else None,
            about=user_profile.about,
            body_weight=user_profile.body_weight,
        )
