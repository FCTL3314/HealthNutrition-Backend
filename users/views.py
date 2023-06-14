from django.conf import settings
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView

from common.views import LogoutRequiredMixin, TitleMixin
from users import forms as user_forms
from users.mixins import ProfileMixin
from users.models import EmailVerification, User
from users.tasks import send_verification_email
from utils.urls import get_referer_or_default


class RegistrationCreateView(
    LogoutRequiredMixin, TitleMixin, SuccessMessageMixin, CreateView
):
    model = User
    form_class = user_forms.RegistrationForm
    template_name = "users/auth/registration.html"
    title = "Sign Up"
    success_message = "You have successfully registered!"
    success_url = reverse_lazy("users:login")


class LoginView(LogoutRequiredMixin, TitleMixin, auth_views.LoginView):
    form_class = user_forms.LoginForm
    template_name = "users/auth/login.html"
    title = "Log In"

    def get(self, request, *args, **kwargs):
        request.session["before_login_url"] = get_referer_or_default(self.request, None)
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        before_login_url = self.request.session.get("before_login_url")
        return (
            before_login_url
            if before_login_url
            else reverse_lazy("products:product-types")
        )

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
        return get_referer_or_default(self.request)


class ProfileAccountView(ProfileMixin, SuccessMessageMixin, TitleMixin, UpdateView):
    model = User
    form_class = user_forms.ProfileForm
    title = "Account"
    success_message = "Profile updated successfully!"

    def get_success_url(self):
        return reverse_lazy("users:profile", args=(self.object.slug,))

    def form_invalid(self, form):
        self.object.refresh_from_db()
        return super().form_invalid(form)


class ProfilePasswordView(
    ProfileMixin, SuccessMessageMixin, TitleMixin, auth_views.PasswordChangeView
):
    form_class = user_forms.PasswordChangeForm
    title = "Password"
    success_message = "Your password has been successfully updated!"

    def get_success_url(self):
        return reverse_lazy("users:profile-password", args={self.request.user.slug})


class ProfileEmailView(
    ProfileMixin, SuccessMessageMixin, TitleMixin, auth_views.PasswordChangeView
):
    form_class = user_forms.EmailChangeForm
    title = "Email"
    success_message = "Your email has been successfully changed!"

    def get_success_url(self):
        return reverse_lazy("users:profile-email", args={self.request.user.slug})


class BaseEmailVerificationView(TitleMixin, LoginRequiredMixin, TemplateView):
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
        seconds_since_last_sending = (
            self.user.seconds_since_last_email_verification_sending()
        )

        if self.user.is_verified:
            messages.warning(request, "You have already verified your email.")
        elif seconds_since_last_sending < settings.EMAIL_SEND_INTERVAL_SECONDS:
            seconds_left = (
                settings.EMAIL_SEND_INTERVAL_SECONDS - seconds_since_last_sending
            )
            messages.warning(
                request, f"Please wait {seconds_left} to resend the confirmation email."
            )
        else:
            verification = self.user.create_email_verification()
            send_verification_email.delay(object_id=verification.id)
        return super().get(request, *args, **kwargs)


class EmailVerificationView(BaseEmailVerificationView):
    template_name = "users/email/email_verification_complete.html"
    title = "Verify"

    def get(self, request, *args, **kwargs):
        code = kwargs.get("code")

        verification = get_object_or_404(EmailVerification, user=self.user, code=code)

        if self.user.is_verified:
            messages.warning(request, "Your email has already been verified.")
        elif verification.is_expired():
            messages.warning(request, "The verification link has expired.")
        else:
            self.user.verify()
        return super().get(request, *args, **kwargs)


class PasswordResetView(
    LogoutRequiredMixin, SuccessMessageMixin, auth_views.PasswordResetView
):
    title = "Password Reset"
    template_name = "users/password/reset_password.html"
    subject_template_name = "users/password/password_reset_subject.html"
    email_template_name = "users/password/password_reset_content.html"
    form_class = user_forms.PasswordResetForm
    success_url = reverse_lazy("users:reset_password")
    success_message = (
        "We’ve emailed you instructions for setting your password, if an account exists with the email "
        "you entered. You should receive them shortly. If you don’t receive an email, please make sure "
        "you’ve entered the address you registered with, and check your spam folder."
    )


class PasswordResetConfirmView(
    LogoutRequiredMixin,
    SuccessMessageMixin,
    TitleMixin,
    auth_views.PasswordResetConfirmView,
):
    title = "Password Reset"
    template_name = "users/password/password_reset_confirm.html"
    form_class = user_forms.SetPasswordForm
    success_url = reverse_lazy("users:login")
    success_message = "Your password has been set. You can now sign into your account with the new password."
