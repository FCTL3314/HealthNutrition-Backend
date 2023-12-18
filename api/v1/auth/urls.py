from django.urls import path

from api.v1.auth.views import (
    CheckUIDAndToken,
)

app_name = "auth"


urlpatterns = [
    path("uid-token-check/", CheckUIDAndToken.as_view(), name="uid-token-check"),
]
