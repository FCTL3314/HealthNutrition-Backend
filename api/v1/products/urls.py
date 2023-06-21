from django.urls import include, path
from rest_framework import routers

from api.v1.products.views import ProductTypeModelViewSet, ProductModelViewSet

app_name = "products"

router = routers.DefaultRouter()

router.register("product-types", ProductTypeModelViewSet, basename="product-types")
router.register("products", ProductModelViewSet, basename="products")

urlpatterns = [
    path("", include(router.urls)),
]
