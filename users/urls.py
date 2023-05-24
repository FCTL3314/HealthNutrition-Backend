from django.urls import path

from users.views import LoginView, LogoutView, RegistrationCreateView, ProfileView, ProfilePasswordView

app_name = 'users'

urlpatterns = [
    path('registration/', RegistrationCreateView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/<slug:slug>/', ProfileView.as_view(), name='profile'),
    path('user/<slug:slug>/password', ProfilePasswordView.as_view(), name='profile-password'),
]
