from typing import Any

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers

User = get_user_model()


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
