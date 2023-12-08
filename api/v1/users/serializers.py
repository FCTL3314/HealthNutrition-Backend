from typing import Any

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from djoser.serializers import UserCreateSerializer as DjoserUserCreateSerializer
from djoser.serializers import UserSerializer as DjoserUserSerializer
from rest_framework import serializers

from api.v1.users.constants import EV_CODE_LENGTH
from api.v1.users.models import EmailVerification, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "image",
            "username",
            "first_name",
            "last_name",
            "about",
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


class CurrentUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + DjoserUserSerializer.Meta.fields


class UserCreateSerializer(DjoserUserCreateSerializer):
    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + DjoserUserCreateSerializer.Meta.fields


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


class UIDAndTokenSerializer(serializers.Serializer):
    uid = serializers.SlugField()
    token = serializers.SlugField()

    @staticmethod
    def validate(data: dict[str, Any]) -> bool:
        try:
            uid = urlsafe_base64_decode(data["uid"])
            user = User.objects.get(pk=uid)
        except (ValueError, User.DoesNotExist):
            raise serializers.ValidationError("Invalid user id or user doesn't exist.")

        if default_token_generator.check_token(user, data["token"]):
            return True
        raise serializers.ValidationError("Invalid token for given user.")
