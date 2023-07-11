from django.urls import include, path

app_name = "interactions"

urlpatterns = [
    path("comments/", include("interactions.comments.urls", namespace="comments")),
]
