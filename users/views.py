from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView

from common import views as common_views
from users import forms
from users.mixins import ProfileMixin
from users.models import User
from users.services import EmailVerificationSender, UserEmailVerifier
from utils.urls import get_referer_or_default


class RegistrationCreateView(
    common_views.LogoutRequiredMixin,
    common_views.TitleMixin,
    SuccessMessageMixin,
    CreateView,
):
    model = User
    form_class = forms.RegistrationForm
    template_name = "users/auth/registration.html"
    title = "Sign Up"
    success_message = "You have successfully registered!"
    success_url = reverse_lazy("users:login")


class LoginView(
    common_views.LogoutRequiredMixin, common_views.TitleMixin, auth_views.LoginView
):
    form_class = forms.LoginForm
    template_name = "users/auth/login.html"
    title = "Log In"

    def get(self, request, *args, **kwargs):
        request.session["before_login_url"] = get_referer_or_default(self.request, None)
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        before_login_url = self.request.session.get("before_login_url")
        return before_login_url or reverse_lazy("products:product-types")

    def form_valid(self, form):
        remember_me = form.cleaned_data.get("remember_me")
        if not remember_me:
            self.request.session.set_expiry(0)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(
            self.request, "The entered data is incorrect, please try again."
        )
        return super().form_invalid(form)


class LogoutView(auth_views.LogoutView):
    def get_redirect_url(self):
        return reverse_lazy("users:login")


class ProfileView(common_views.TitleMixin, DetailView):
    model = User
    template_name = "users/profile/profile.html"

    def get_title(self):
        return f"{self.object.username}'s Profile"


class AccountSettingsView(
    ProfileMixin, SuccessMessageMixin, common_views.TitleMixin, UpdateView
):
    model = User
    form_class = forms.UserChangeForm
    title = "Account"
    success_message = "Profile updated successfully!"

    def get_success_url(self):
        return reverse_lazy("users:profile-account")

    def form_invalid(self, form):
        self.object.refresh_from_db()
        return super().form_invalid(form)


class PasswordSettingsView(
    ProfileMixin,
    SuccessMessageMixin,
    common_views.TitleMixin,
    auth_views.PasswordChangeView,
):
    form_class = forms.PasswordChangeForm
    title = "Password"
    success_message = "Your password has been successfully updated!"

    def get_success_url(self):
        return reverse_lazy("users:profile-password")


class EmailSettingsView(
    ProfileMixin,
    SuccessMessageMixin,
    common_views.TitleMixin,
    auth_views.PasswordChangeView,
):
    form_class = forms.EmailChangeForm
    title = "Email"
    success_message = "Your email has been successfully changed!"

    def get_success_url(self):
        return reverse_lazy("users:profile-email")


class BaseEmailVerificationView(
    common_views.TitleMixin, LoginRequiredMixin, TemplateView
):
    user: User = None

    def dispatch(self, request, *args, **kwargs):
        email = kwargs.get("email")
        self.user = get_object_or_404(User, email=email)
        if not self.user.is_request_user_matching(request):
            raise Http404
        return super().dispatch(request, *args, **kwargs)


class SendVerificationEmailView(BaseEmailVerificationView):
    template_name = "users/email/email_verification_done.html"
    title = "Send Verification"

    def get(self, request, *args, **kwargs):
        sender_service = EmailVerificationSender(request)
        sender_service.send()
        return super().get(request, *args, **kwargs)


class EmailVerificationView(BaseEmailVerificationView):
    template_name = "users/email/email_verification_complete.html"
    title = "Verify"

    def get(self, request, *args, **kwargs):
        code = kwargs.get("code")
        verifier_service = UserEmailVerifier(request, code)
        verifier_service.verify()
        return super().get(request, *args, **kwargs)


class PasswordResetView(
    common_views.LogoutRequiredMixin, SuccessMessageMixin, auth_views.PasswordResetView
):
    title = "Password Reset"
    template_name = "users/password/reset_password.html"
    subject_template_name = "users/password/password_reset_subject.html"
    email_template_name = "users/password/password_reset_content.html"
    form_class = forms.PasswordResetForm
    success_url = reverse_lazy("users:reset_password")
    success_message = (
        "We’ve emailed you instructions for setting your password, if an account exists with the email "
        "you entered. You should receive them shortly. If you don’t receive an email, please make sure "
        "you’ve entered the address you registered with, and check your spam folder."
    )


class PasswordResetConfirmView(
    common_views.LogoutRequiredMixin,
    SuccessMessageMixin,
    common_views.TitleMixin,
    auth_views.PasswordResetConfirmView,
):
    title = "Password Reset"
    template_name = "users/password/password_reset_confirm.html"
    form_class = forms.SetPasswordForm
    success_url = reverse_lazy("users:login")
    success_message = "Your password has been set. You can now sign into your account with the new password."
