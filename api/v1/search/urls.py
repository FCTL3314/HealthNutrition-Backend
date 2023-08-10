from django.urls import path

from api.v1.search.views import ProductSearchListAPIView, ProductTypeSearchListAPIView

app_name = "search"

urlpatterns = [
    path("product-type/", ProductTypeSearchListAPIView.as_view(), name="product-type"),
    path("product/", ProductSearchListAPIView.as_view(), name="product"),
]
