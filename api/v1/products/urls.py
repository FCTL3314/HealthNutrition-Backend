from django.urls import include, path
from rest_framework import routers

from api.v1.products.views import ProductTypeViewSet, ProductViewSet

app_name = "products"

router = routers.DefaultRouter()
router.register("product-types", ProductTypeViewSet, basename="product-types")
router.register("", ProductViewSet, basename="products")

urlpatterns = [
    path("", include(router.urls)),
]
