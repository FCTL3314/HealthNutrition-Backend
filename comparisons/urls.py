from django.urls import path

from comparisons.views import (ComparisonProductListView,
                               ComparisonProductTypeListView)

app_name = 'comparisons'

urlpatterns = [
    path('', ComparisonProductTypeListView.as_view(), name='product-type-comparisons'),
    path('<slug:slug>/', ComparisonProductListView.as_view(), name='product-comparisons'),
]
