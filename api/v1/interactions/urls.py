from django.urls import path, include

app_name = "interactions"

urlpatterns = [
    path("comment/", include("api.v1.interactions.comments.urls", namespace="comments")),
]
