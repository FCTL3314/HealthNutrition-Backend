from django.urls import include, path
from rest_framework import routers

from api.v1.categories.views import CategoryViewSet

app_name = "categories"

router = routers.DefaultRouter()
router.register("", CategoryViewSet, basename="categories")

urlpatterns = [
    path("", include(router.urls)),
]
