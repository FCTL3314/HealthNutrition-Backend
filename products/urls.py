from django.urls import path

from products.views import (ProductDetailView, ProductListView,
                            ProductSearchListView, ProductTypeListView,
                            ProductTypeSearchListView, SearchRedirectView)

app_name = 'products'

urlpatterns = [
    path('', ProductTypeListView.as_view(), name='product-types'),
    path('products/<slug:slug>/', ProductListView.as_view(), name='products'),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),
    path('search/redirect/', SearchRedirectView.as_view(), name='search-redirect'),
    path('search/products/', ProductSearchListView.as_view(), name='product-search'),
    path('search/product-types/', ProductTypeSearchListView.as_view(), name='product-type-search'),
]
