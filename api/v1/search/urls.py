from django.urls import path

from api.v1.search.views import ProductSearchListView, ProductTypeSearchListView

app_name = "search"

urlpatterns = [
    path("product-type/", ProductTypeSearchListView.as_view(), name="product-type"),
    path("product/", ProductSearchListView.as_view(), name="product"),
]
