from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.timezone import now

from api.common.models.mixins import SlugModelMixin
from api.utils.codes import generate_digits_code
from api.v1.users.constants import (
    EV_CODE_LENGTH,
)
from api.v1.users.managers import EmailVerificationManager
from api.v1.users.services.infrastructure.get_email_verification_expiration import (
    get_email_verification_expiration,
)

USER_SLUG_RELATED_FIELD = "username"


class User(SlugModelMixin, AbstractUser):
    profile = models.OneToOneField(
        to="user_profiles.UserProfile", related_name="user", on_delete=models.PROTECT
    )
    email = models.EmailField(unique=True)
    comparison_groups = models.ManyToManyField(
        "comparisons.ComparisonGroup",
        through="comparisons.Comparison",
        blank=True,
    )
    comments = GenericRelation("comments.Comment")
    is_verified = models.BooleanField(default=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._meta.get_field(self.USERNAME_FIELD).validators = (
            ASCIIUsernameValidator(),
        )

    def __str__(self):
        return self.username

    def update_email(self, new_email: str) -> None:
        self.email = new_email
        self.save()

    def verify(self, commit=True) -> None:
        if not self.is_verified:
            self.is_verified = True
            if commit:
                self.save(update_fields=("is_verified",))

    def make_unverified(self, commit=True) -> None:
        if self.is_verified:
            self.is_verified = False
            if commit:
                self.save(update_fields=("is_verified",))

    def change_slug(self, commit=True) -> None:
        self.slug = slugify(getattr(self, USER_SLUG_RELATED_FIELD))
        if commit:
            self.save(update_fields=("slug",))

    def get_absolute_url(self) -> str:
        return reverse("api:v1:users:users-detail", args=(self.slug,))


class EmailVerification(models.Model):
    code = models.CharField(null=True, max_length=EV_CODE_LENGTH)
    user = models.ForeignKey(to="users.User", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField(default=get_email_verification_expiration)

    objects = EmailVerificationManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("code", "user"),
                name="unique_code_and_email",
            )
        ]

    def __str__(self):
        return f"{self.user.email} | {self.expiration}"

    def save(self, *args, **kwargs):
        self.code = self.generate_code()
        super().save(*args, **kwargs)

    def generate_code(self) -> str:
        code = generate_digits_code(EV_CODE_LENGTH)
        if EmailVerification.objects.filter(code=code, user=self.user).exists():
            return self.generate_code()
        return code

    @property
    def is_expired(self) -> bool:
        return self.expiration < now()
