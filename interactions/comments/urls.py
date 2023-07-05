from django.urls import path

from interactions.comments import views

app_name = "comments"

urlpatterns = [
    path("store/<slug:slug>/add", views.StoreCommentCreateView.as_view(), name="store-add"),
    path("product/<slug:slug>/add", views.ProductCommentCreateView.as_view(), name="product-add"),
]
