from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.v1.comments.views import ProductCommentModelViewSet

app_name = "comments"


router = DefaultRouter()
router.register("product", ProductCommentModelViewSet, basename="product")

urlpatterns = [
    path("", include(router.urls)),
]
