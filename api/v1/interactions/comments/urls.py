from django.urls import path

from api.v1.interactions.comments import views

app_name = "comments"

urlpatterns = [
    path("store/add/", views.StoreCommentCreateAPIView.as_view(), name="store-add"),
    path("product/add/", views.ProductCommentCreateAPIView.as_view(), name="product-add"),
]
