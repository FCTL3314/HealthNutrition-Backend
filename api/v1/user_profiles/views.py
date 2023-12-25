from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from api.v1.user_profiles.models import UserProfile
from api.v1.user_profiles.permissions import IsProfileOwner
from api.v1.user_profiles.serializers import UserProfileSerializer


class UserProfileUpdateView(UpdateAPIView):
    queryset = UserProfile.objects.all()
    permission_classes = (IsAuthenticated, IsProfileOwner)
    serializer_class = UserProfileSerializer
