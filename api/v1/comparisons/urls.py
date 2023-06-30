from django.urls import include, path
from rest_framework import routers

from api.v1.comparisons.views import ComparisonProductGenericViewSet, ComparisonProductTypeModelViewSet

app_name = "comparisons"

router = routers.DefaultRouter()

router.register("product-types", ComparisonProductTypeModelViewSet, basename="product-type-comparisons")
router.register("products", ComparisonProductGenericViewSet, basename="product-comparisons")

urlpatterns = [
    path("", include(router.urls)),
]
