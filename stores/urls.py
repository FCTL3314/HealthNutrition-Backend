from django.urls import path

from stores.views import StoreDetailView

app_name = 'stores'

urlpatterns = [
    path('<slug:slug>/', StoreDetailView.as_view(), name='store-detail'),
]
