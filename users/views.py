from django.contrib.auth import views as auth_views
from django.views.generic.edit import CreateView

from users.forms import LoginForm, RegistrationForm
from users.models import User
from utils.common.views import LogoutRequiredMixin, TitleMixin


class RegistrationCreateView(LogoutRequiredMixin, TitleMixin, CreateView):
    model = User
    form_class = RegistrationForm
    template_name = 'users/registration.html'
    title = 'Sign Up'


class LoginView(LogoutRequiredMixin, TitleMixin, auth_views.LoginView):
    form_class = LoginForm
    template_name = 'users/login.html'
    title = 'Log In'
