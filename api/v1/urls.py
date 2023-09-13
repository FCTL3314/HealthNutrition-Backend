from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.v1.schema_urls import urlpatterns as schema_urlpatterns

app_name = "v1"

urlpatterns = [
    path("stores/", include("api.v1.stores.urls", namespace="stores")),
    path("products/", include("api.v1.products.urls", namespace="products")),
    path("comparisons/", include("api.v1.comparisons.urls", namespace="comparisons")),
    path("users/", include("api.v1.users.urls", namespace="users")),
    path("comments/", include("api.v1.comments.urls", namespace="comments")),
    path("token/", TokenObtainPairView.as_view(), name="token-obtain-pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
]
urlpatterns += schema_urlpatterns
