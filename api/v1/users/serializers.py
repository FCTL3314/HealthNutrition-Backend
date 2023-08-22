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


class EmailVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailVerification
        fields = ("expiration", "created_at")


class UserVerificationSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=EV_CODE_LENGTH)
