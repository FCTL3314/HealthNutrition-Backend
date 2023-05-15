from django.contrib.auth.views import LogoutView
from django.urls import path

from users.views import LoginView, RegistrationCreateView

app_name = 'users'

urlpatterns = [
    path('registration/', RegistrationCreateView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
