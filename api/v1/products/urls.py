from django.urls import include, path
from rest_framework import routers

from api.v1.products.views import ProductViewSet

app_name = "products"

router = routers.DefaultRouter()
router.register("", ProductViewSet, basename="products")

urlpatterns = [
    path("", include(router.urls)),
]
