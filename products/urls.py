from django.urls import include, path
from rest_framework import routers

from products.views import ProductModelViewSet, ProductTypeModelViewSet

app_name = "products"

router = routers.DefaultRouter()
router.register("product-types", ProductTypeModelViewSet, basename="product-types")
router.register("", ProductModelViewSet, basename="products")

urlpatterns = [
    path("", include(router.urls)),
]
