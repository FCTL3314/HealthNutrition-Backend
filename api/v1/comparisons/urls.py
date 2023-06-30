from django.urls import include, path
from rest_framework import routers

from api.v1.comparisons.views import ComparisonProductModelViewSet, ComparisonProductTypeModelViewSet

app_name = "comparisons"

router = routers.DefaultRouter()

router.register("product-types", ComparisonProductTypeModelViewSet, basename="product-type-comparisons")
router.register("products", ComparisonProductModelViewSet, basename="product-comparisons")

urlpatterns = [
    path("", include(router.urls)),
]
