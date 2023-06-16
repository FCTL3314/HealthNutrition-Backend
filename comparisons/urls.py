from django.urls import path

from comparisons import views

app_name = "comparisons"

urlpatterns = [
    path("", views.ComparisonProductTypeListView.as_view(), name="product-type-comparisons"),
    path("<slug:slug>/", views.ComparisonProductListView.as_view(), name="product-comparisons"),
]
