from django.urls import include, path

app_name = "interactions"

urlpatterns = [
    path("comment/", include("api.v1.interactions.comments.urls", namespace="comments")),
]
