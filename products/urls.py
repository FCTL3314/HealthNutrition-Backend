from django.urls import path

from products.views import (ProductsListView, ProductTypeListView,
                            ProductTypeProductsListView, SearchRedirectView)

app_name = 'products'

urlpatterns = [
    path('', ProductTypeListView.as_view(), name='product-types'),
    path('products/<slug:slug>/', ProductTypeProductsListView.as_view(), name='product-type-products'),
    path('products/', ProductsListView.as_view(), name='products'),
    path('search/', SearchRedirectView.as_view(), name='search-redirect'),
]
