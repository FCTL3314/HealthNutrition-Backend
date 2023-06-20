from django.urls import path

from users import views

app_name = "users"

urlpatterns = [
    path("registration/", views.RegistrationCreateView.as_view(), name="registration"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),

    path("verification/send/<str:email>/", views.SendVerificationEmailView.as_view(), name="send-verification-email"),
    path("verify/<str:email>/<uuid:code>/", views.EmailVerificationView.as_view(), name="email-verification"),

    path("password_reset/", views.PasswordResetView.as_view(), name="reset_password"),
    path("reset/<uidb64>/<token>/", views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),

    path("<slug:slug>/", views.ProfileView.as_view(), name="profile"),
    path("<slug:slug>/account/", views.ProfileSettingsAccountView.as_view(), name="profile-account"),
    path("<slug:slug>/password/", views.ProfileSettingsPasswordView.as_view(), name="profile-password"),
    path("<slug:slug>/email/", views.ProfileSettingsEmailView.as_view(), name="profile-email"),
]
