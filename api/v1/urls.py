from django.urls import include, path

app_name = "v1"

urlpatterns = [
    path("stores/", include("api.v1.stores.urls", namespace="stores")),
    path("products/", include("api.v1.products.urls", namespace="products")),
]
