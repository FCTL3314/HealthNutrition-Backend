from django.urls import path

from comparisons.views import ComparisonProductTypeListView

app_name = 'comparisons'

urlpatterns = [
    path('', ComparisonProductTypeListView.as_view(), name='product-type-comparisons'),
]
