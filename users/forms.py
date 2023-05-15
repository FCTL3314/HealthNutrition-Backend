from django import forms
from django.contrib.auth import forms as auth_forms

from users.models import User


class RegistrationForm(auth_forms.UserCreationForm):
    username = forms.CharField(
        min_length=4,
        max_length=32,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter username',
                'type': 'text',
            }
        )
    )
    email = forms.EmailField(
        max_length=255,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter email',
                'type': 'email',
            }
        )
    )
    password1 = forms.CharField(
        max_length=32,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter password',
                'type': 'password',
            }
        )
    )
    password2 = forms.CharField(
        max_length=32,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter password confirmation',
                'type': 'password',
            }
        )
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginForm(auth_forms.AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter username',
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter password',
            }
        )
    )
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input',
            }
        )
    )

    class Meta:
        model = User
        fields = ('username', 'password', 'remember_me')
