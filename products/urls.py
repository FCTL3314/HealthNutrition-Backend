from django.urls import path

from products.views import ProductTypeView, ProductView

app_name = 'products'

urlpatterns = [
    path('', ProductTypeView.as_view(), name='product-types'),
    path('products/<slug:product_type>/', ProductView.as_view(), name='products'),
]
