from django.urls import include, path

from users import views

app_name = "users"

settings_paths = [
    path("account/", views.AccountSettingsView.as_view(), name="profile-account"),
    path("password/", views.PasswordSettingsView.as_view(), name="profile-password"),
    path("email/", views.EmailSettingsView.as_view(), name="profile-email"),
]

urlpatterns = [
    path("registration/", views.RegistrationCreateView.as_view(), name="registration"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),

    path("verification/send/<str:email>/", views.SendVerificationEmailView.as_view(), name="send-verification-email"),
    path("verify/<str:email>/<uuid:code>/", views.EmailVerificationView.as_view(), name="email-verification"),

    path("password_reset/", views.PasswordResetView.as_view(), name="reset_password"),
    path("reset/<uidb64>/<token>/", views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),

    path("<slug:slug>/", views.ProfileView.as_view(), name="profile"),
    path("settings/", include(settings_paths)),
]
