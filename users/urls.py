from django.urls import path

import users.views as user_views

app_name = 'users'

urlpatterns = [
    path('registration/', user_views.RegistrationCreateView.as_view(), name='registration'),
    path('login/', user_views.LoginView.as_view(), name='login'),
    path('logout/', user_views.LogoutView.as_view(), name='logout'),

    path('verification/send/<str:email>/', user_views.SendVerificationEmailView.as_view(),
         name='send-verification-email'),
    path('verify/<str:email>/<uuid:code>/', user_views.EmailVerificationView.as_view(), name='email-verification'),

    path('password_reset/', user_views.PasswordResetView.as_view(), name='reset_password'),
    path('reset/<uidb64>/<token>/', user_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    path('<slug:slug>/', user_views.ProfileView.as_view(), name='profile'),
    path('<slug:slug>/password', user_views.ProfilePasswordView.as_view(), name='profile-password'),
    path('<slug:slug>/email', user_views.ProfileEmailView.as_view(), name='profile-email'),
]
