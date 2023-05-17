from django.urls import path

from products.views import IndexListView, ProductListView

app_name = 'products'

urlpatterns = [
    path('', IndexListView.as_view(), name='index'),
    path('products/<slug:product_type>/', ProductListView.as_view(), name='products'),
]
