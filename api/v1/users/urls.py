from django.urls import include, path
from djoser.views import UserViewSet
from rest_framework import routers

from api.v1.users.constants import ALLOWED_DJOSER_ENDPOINTS
from api.v1.users.views import EmailVerificationCreateAPIView, VerifyUserUpdateAPIView

app_name = "users"

djoser_router = routers.DefaultRouter()
djoser_router.register("", UserViewSet, basename="users")

djoser_paths = [
    url for url in djoser_router.urls if url.name in ALLOWED_DJOSER_ENDPOINTS  # type: ignore[union-attr, operator]
]

verification_paths = [
    path("send/", EmailVerificationCreateAPIView.as_view(), name="verification-send"),
    path("verify/", VerifyUserUpdateAPIView.as_view(), name="verify"),
]

urlpatterns = [
    path("", include(djoser_paths)),
    path("verification/", include(verification_paths)),
]
