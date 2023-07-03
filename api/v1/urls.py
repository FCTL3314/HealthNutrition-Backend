from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = "v1"

urlpatterns = [
    path("stores/", include("api.v1.stores.urls", namespace="stores")),
    path("products/", include("api.v1.products.urls", namespace="products")),
    path("comparisons/", include("api.v1.comparisons.urls", namespace="comparisons")),
    path("users/", include("api.v1.users.urls", namespace="users")),

    path("token/", TokenObtainPairView.as_view(), name="token-obtain-pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
]
