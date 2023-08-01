from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/stores/", include("stores.urls", namespace="stores")),
    path("api/v1/products/", include("products.urls", namespace="products")),
    path("api/v1/comparisons/", include("comparisons.urls", namespace="comparisons")),
    path("api/v1/users/", include("users.urls", namespace="users")),
    path("api/v1/token/", TokenObtainPairView.as_view(), name="token-obtain-pair"),
    path("api/v1/token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls))
    ] + urlpatterns  # TODO: Remove ?
