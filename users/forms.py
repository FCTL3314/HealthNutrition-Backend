from django import forms
from django.contrib.auth import forms as auth_forms
from django.core.exceptions import ValidationError

from users.models import User
from users.tasks import send_password_reset_email


class RegistrationForm(auth_forms.UserCreationForm):
    username = forms.CharField(
        min_length=4,
        max_length=32,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter username",
                "type": "text",
            }
        ),
    )
    email = forms.EmailField(
        max_length=255,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter email",
                "type": "email",
            }
        ),
    )
    password1 = forms.CharField(
        max_length=32,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter password",
                "type": "password",
            }
        ),
    )
    password2 = forms.CharField(
        max_length=32,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter password confirmation",
                "type": "password",
            }
        ),
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class LoginForm(auth_forms.AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter username",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter password",
            }
        )
    )
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-check-input",
            }
        ),
    )

    class Meta:
        model = User
        fields = ("username", "password", "remember_me")


class ProfileForm(auth_forms.UserChangeForm):
    username = forms.CharField(
        min_length=4,
        max_length=32,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
            }
        ),
    )
    first_name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
                "placeholder": "Enter your first name",
            }
        ),
    )
    last_name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
                "placeholder": "Enter your last name",
            }
        ),
    )
    email = forms.EmailField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "readonly": True,
            }
        )
    )
    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(
            attrs={
                "class": "form-control",
                "type": "file",
                "aria-label": "Upload",
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial["email"] = self.instance.email

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "image")


class PasswordChangeForm(auth_forms.PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your old password",
            }
        )
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your new password",
            }
        )
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter password confirmation",
            }
        )
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(user, *args, **kwargs)

    def clean(self):
        super().clean()
        new_password1 = self.data["new_password1"]
        if self.user.check_password(new_password1):
            raise forms.ValidationError(
                "The new password must be different from the old one."
            )

    class Meta:
        model = User
        fields = ("old_password", "new_password1", "new_password2")


class EmailChangeForm(forms.Form):
    new_email = forms.CharField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter Email",
            }
        )
    )
    old_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your password",
            }
        )
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_old_password(self):
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise ValidationError(
                "Your old password was entered incorrectly. Please try again."
            )
        return old_password

    def clean_new_email(self):
        new_email = self.cleaned_data.get("new_email")
        if self.user.email == new_email:
            raise forms.ValidationError("You're already using this email address.")
        if User.objects.filter(email=new_email).exists():
            raise forms.ValidationError(
                "This email address is already in use. Please use a different email address."
            )
        return new_email

    def save(self, commit=True):
        self.user.email = self.cleaned_data["new_email"]
        self.user.is_verified = False
        if commit:
            self.user.save()
        return self.user


class PasswordResetForm(auth_forms.PasswordResetForm):
    email = forms.CharField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter Email",
            }
        )
    )

    def send_mail(
        self,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None,
    ):
        context["user"] = context["user"].id
        send_password_reset_email.delay(
            subject_template_name, email_template_name, to_email, context
        )

    class Meta:
        model = User
        fields = ("email",)


class SetPasswordForm(auth_forms.SetPasswordForm):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter new password",
            }
        )
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Confirm new password",
            }
        )
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        self.user = user

    def clean_new_password2(self):
        new_password = self.cleaned_data["new_password1"]
        if self.user.check_password(new_password):
            raise forms.ValidationError(
                "The new password must be different from the old one."
            )
        return super().clean_new_password2()

    class Meta:
        model = User
        fields = ("new_password1", "new_password2")
