from django.urls import path

from interactions.comments import views

app_name = "comments"

urlpatterns = [
    path("product/<slug:slug>/add", views.ProductCommentView.as_view(), name="product-add"),
    path("store/<slug:slug>/add", views.StoreCommentView.as_view(), name="store-add"),
]
