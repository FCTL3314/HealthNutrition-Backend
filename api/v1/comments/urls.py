from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.v1.comments.views import ProductCommentViewSet, StoreCommentViewSet

app_name = "comments"


router = DefaultRouter()
router.register("product", ProductCommentViewSet, basename="product")
router.register("store", StoreCommentViewSet, basename="store")

urlpatterns = [
    path("", include(router.urls)),
]
