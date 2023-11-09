from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.v1.comparisons.views import ComparisonsViewSet, ComparisonGroupViewSet

app_name = "comparisons"

router = DefaultRouter()
router.register("groups", ComparisonGroupViewSet, basename="comparison-groups")
router.register("", ComparisonsViewSet, basename="comparisons")

urlpatterns = [
    path("", include(router.urls)),
]
