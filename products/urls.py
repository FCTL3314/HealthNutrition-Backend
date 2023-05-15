from django.urls import path

from products.views import IndexListView

app_name = 'products'

urlpatterns = [
    path('', IndexListView.as_view(), name='index'),
]
