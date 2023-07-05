from django.urls import include, path

app_name = "interactions"

urlpatterns = [
    path("comment/", include("interactions.comments.urls")),
]
