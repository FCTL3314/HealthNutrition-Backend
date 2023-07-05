from rest_framework import serializers

from users.models import EmailVerification, User


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "image",
            "username",
            "first_name",
            "last_name",
            "about",
            "email",
            "is_verified",
            "slug",
            "date_joined",
            "last_login",
        )
        read_only_fields = ("slug", "date_joined", "last_login", "is_verified")


class EmailVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailVerification
        fields = ("expiration", "created_at")


class SendVerificationEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class VerifyUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.UUIDField()
