from rest_framework import serializers

from api.v1.user_profiles.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            "id",
            "image",
            "about",
            "body_weight",
        )
