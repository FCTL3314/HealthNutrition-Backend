from django.urls import include, path
from rest_framework import routers

from stores.views import StoreModelViewSet

app_name = "stores"

router = routers.DefaultRouter()
router.register("", StoreModelViewSet, basename="stores")

urlpatterns = [
    path("", include(router.urls)),
]
