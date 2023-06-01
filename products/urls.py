from django.urls import path

from products.views import (ProductDetailView, ProductListView,
                            ProductTypeListView, SearchListView)

app_name = 'products'

urlpatterns = [
    path('', ProductTypeListView.as_view(), name='product-types'),
    path('products/<slug:slug>/', ProductListView.as_view(), name='products'),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),
    path('search/', SearchListView.as_view(), name='search'),
]
