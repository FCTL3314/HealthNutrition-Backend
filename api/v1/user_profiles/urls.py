from django.urls import path

from api.v1.user_profiles.views import UserProfileUpdateView

app_name = "users"

urlpatterns = [
    path(
        "profile/update/", UserProfileUpdateView.as_view(), name="user-profile-update"
    ),
]
