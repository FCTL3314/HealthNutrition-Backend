from typing import Any

from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer as DjoserUserCreateSerializer
from djoser.serializers import UserSerializer as DjoserUserSerializer
from rest_framework import serializers

from api.v1.user_profiles.serializers import UserProfileSerializer
from api.v1.users.constants import EV_CODE_LENGTH
from api.v1.users.models import EmailVerification
from api.v1.users.services.infrastructure.user_create import create_user_with_profile

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "is_verified",
            "slug",
            "date_joined",
            "last_login",
            "is_staff",
        )
        read_only_fields = (
            "slug",
            "date_joined",
            "last_login",
            "is_verified",
            "is_staff",
        )


class UserWithProfileSerializer(UserSerializer):
    profile = UserProfileSerializer(read_only=True)

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ("profile",)


class CurrentUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + DjoserUserSerializer.Meta.fields


class CurrentUserWithProfileSerializer(UserWithProfileSerializer):
    class Meta(UserWithProfileSerializer.Meta):
        fields = (
            UserWithProfileSerializer.Meta.fields + DjoserUserSerializer.Meta.fields
        )


class UserCreateSerializer(DjoserUserCreateSerializer, UserWithProfileSerializer):
    class Meta(UserWithProfileSerializer.Meta):
        fields = (
            UserWithProfileSerializer.Meta.fields
            + DjoserUserCreateSerializer.Meta.fields
        )

    @staticmethod
    def perform_create(validated_data: dict[str, Any]) -> User:
        return create_user_with_profile(validated_data)


class UserChangeEmailSerializer(serializers.Serializer):
    new_email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class EmailVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailVerification
        fields = ("expiration", "created_at")
        read_only_fields = ("expiration", "created_at")


class UserVerificationSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=EV_CODE_LENGTH)
