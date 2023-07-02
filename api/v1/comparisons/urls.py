from django.urls import path

from api.v1.comparisons.views import ComparisonProductTypeListAPIView, ComparisonProductListAPIView

app_name = "comparisons"

urlpatterns = [
    path("product-types/", ComparisonProductTypeListAPIView.as_view(), name="product-types"),
    path("products/<slug:slug>/", ComparisonProductListAPIView.as_view(), name="products"),
]
