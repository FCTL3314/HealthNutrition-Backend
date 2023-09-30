from django.urls import include, path
from rest_framework import routers

from api.v1.users.constants import ALLOWED_DJOSER_ENDPOINTS
from api.v1.users.views import (
    UserEmailVerifierView,
    UserSendEmailVerificationView,
    UserViewSet,
)

app_name = "users"

djoser_router = routers.DefaultRouter()
djoser_router.register("", UserViewSet, basename="users")

djoser_paths = [
    url for url in djoser_router.urls if url.name in ALLOWED_DJOSER_ENDPOINTS
]

verification_paths = [
    path("send/", UserSendEmailVerificationView.as_view(), name="verification-send"),
    path("verify/", UserEmailVerifierView.as_view(), name="verify"),
]

urlpatterns = [
    path("verification/", include(verification_paths)),
    path("", include(djoser_paths)),
]
