from django.conf import settings
from django.urls import path, include
from djoser.views import UserViewSet
from rest_framework import routers

app_name = "users"

djoser_router = routers.DefaultRouter()
djoser_router.register("", UserViewSet, basename="users")
filtered_djoser_router_urls = [
    url for url in djoser_router.urls if url.name in settings.ALLOWED_DJOSER_ENDPOINTS
]

urlpatterns = [
    path("", include(filtered_djoser_router_urls)),
]
