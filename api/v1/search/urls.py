from django.urls import path

from api.v1.search.views import ProductTypeSearchListAPIView

app_name = "search"

urlpatterns = [
    path("product-type/", ProductTypeSearchListAPIView.as_view(), name="product-type"),
]
