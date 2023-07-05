from django.urls import include, path

from interactions import views

app_name = "interactions"

comments_paths = [
    path("product/<slug:slug>/add", views.ProductCommentView.as_view(), name="product-comment-add"),
    path("store/<slug:slug>/add", views.StoreCommentView.as_view(), name="store-comment-add"),
]

urlpatterns = [
    path("comment/", include(comments_paths)),
]
