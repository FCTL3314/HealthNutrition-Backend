from django.urls import path

from comparisons import views

app_name = "comparisons"

urlpatterns = [
    path(
        "product-types/",
        views.ComparedProductTypesListAPIView.as_view(),
        name="product-types",
    ),
    path(
        "products/<slug:slug>/",
        views.ComparedProductsListApiView.as_view(),
        name="products",
    ),
    path(
        "add/<int:product_id>/",
        views.ComparisonGenericViewSet.as_view({"post": "create"}),
        name="add",
    ),
    path(
        "remove/<int:product_id>/",
        views.ComparisonGenericViewSet.as_view({"delete": "destroy"}),
        name="remove",
    ),
]
