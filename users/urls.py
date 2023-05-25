from django.urls import path

from users.views import (LoginView, LogoutView, ProfileEmailView,
                         ProfilePasswordView, ProfileView,
                         RegistrationCreateView)

app_name = 'users'

urlpatterns = [
    path('registration/', RegistrationCreateView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('<slug:slug>/', ProfileView.as_view(), name='profile'),
    path('<slug:slug>/password', ProfilePasswordView.as_view(), name='profile-password'),
    path('<slug:slug>/email', ProfileEmailView.as_view(), name='profile-email'),
]
