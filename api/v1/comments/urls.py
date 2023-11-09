from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.v1.comments.views import CommentViewSet

app_name = "comments"

router = DefaultRouter()
router.register("", CommentViewSet, basename="comments")

urlpatterns = [
    path("", include(router.urls)),
]
