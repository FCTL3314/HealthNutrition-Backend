from django.urls import path

from products import views

app_name = 'products'

urlpatterns = [
    path('', views.ProductTypeListView.as_view(), name='product-types'),
    path('products/<slug:slug>/', views.ProductListView.as_view(), name='products'),
    path('product/<slug:slug>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('search/redirect/', views.SearchRedirectView.as_view(), name='search-redirect'),
    path('search/products/', views.ProductSearchListView.as_view(), name='product-search'),
    path('search/product-types/', views.ProductTypeSearchListView.as_view(), name='product-type-search'),
]
