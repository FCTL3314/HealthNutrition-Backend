from django.urls import path

from stores import views

app_name = "stores"

urlpatterns = [
    path("<slug:slug>/", views.StoreDetailView.as_view(), name="store-detail"),
]
