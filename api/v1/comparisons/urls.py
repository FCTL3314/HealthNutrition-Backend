from django.urls import path

from api.v1.comparisons import views

app_name = "comparisons"

urlpatterns = [
    path(
        "product-types/",
        views.ComparedProductTypesListView.as_view(),
        name="product-types",
    ),
    path(
        "products/<slug:product_type_slug>/",
        views.ComparedProductsListView.as_view(),
        name="products",
    ),
    path(
        "add/<int:product_id>/",
        views.ComparisonCreateView.as_view(),
        name="add",
    ),
    path(
        "remove/<int:product_id>/",
        views.ComparisonDestroyView.as_view(),
        name="remove",
    ),
]
