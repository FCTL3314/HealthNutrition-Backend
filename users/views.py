from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.views.generic.edit import UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from users import forms as user_forms
from users.models import User
from utils.common.urls import get_referer_or_default
from utils.common.views import LogoutRequiredMixin, TitleMixin


class RegistrationCreateView(LogoutRequiredMixin, TitleMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = user_forms.RegistrationForm
    template_name = 'users/auth/registration.html'
    title = 'Sign Up'
    success_message = 'You have successfully registered!'
    success_url = reverse_lazy('users:login')


class LoginView(LogoutRequiredMixin, TitleMixin, auth_views.LoginView):
    form_class = user_forms.LoginForm
    template_name = 'users/auth/login.html'
    title = 'Log In'

    def get(self, request, *args, **kwargs):
        request.session['before_login_url'] = get_referer_or_default(self.request, None)
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        before_login_url = self.request.session.get('before_login_url')
        return before_login_url if before_login_url else reverse_lazy('products:product-types')

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')
        if not remember_me:
            self.request.session.set_expiry(0)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, 'The entered data is incorrect, please try again.')
        return super().form_invalid(form)


class LogoutView(auth_views.LogoutView):
    def get_redirect_url(self):
        return get_referer_or_default(self.request)


class ProfileView(TitleMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = user_forms.ProfileForm
    template_name = 'users/profile/profile.html'
    title = 'Account'
    success_message = 'Profile updated successfully!'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.slug,))

    def form_invalid(self, form):
        self.object.refresh_from_db()
        return super().form_invalid(form)


class ProfilePasswordView(SuccessMessageMixin, auth_views.PasswordChangeView):
    form_class = user_forms.PasswordChangeForm
    template_name = 'users/profile/profile.html'
    title = 'Password'
    success_message = 'Your password has been successfully updated!'

    def get_success_url(self):
        return reverse_lazy('users:profile-password', args={self.request.user.slug})
