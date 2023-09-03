import random
from datetime import datetime
from string import digits

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import QuerySet
from django.utils.text import slugify
from django.utils.timezone import now

from api.common.tasks import send_html_mail
from api.decorators import order_queryset
from api.v1.users.constants import EV_CODE_LENGTH, EV_EXPIRATION_TIMEDELTA
from api.v1.users.managers import EmailVerificationManager

USER_SLUG_RELATED_FIELD = "username"


class User(AbstractUser):
    email = models.EmailField(unique=True)
    image = models.ImageField(upload_to="users", null=True, blank=True)
    about = models.TextField(max_length=516, null=True, blank=True)
    slug = models.SlugField(unique=True)
    comparisons = models.ManyToManyField(
        "products.Product", through="comparisons.Comparison", blank=True
    )
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    def create_email_verification(self):
        verification = EmailVerification.objects.create(user=self)
        verification.save()
        return verification

    @order_queryset("-created_at")
    def valid_email_verifications(self) -> QuerySet:
        return self.emailverification_set.filter(expiration__gt=now())

    def update_email(self, new_email: str) -> None:
        self.email = new_email
        self.is_verified = False
        self.save()

    def verify(self, commit=True) -> None:
        if not self.is_verified:
            self.is_verified = True
            if commit:
                self.save(update_fields=("is_verified",))

    def change_slug(self, commit=True) -> None:
        self.slug = slugify(getattr(self, USER_SLUG_RELATED_FIELD))
        if commit:
            self.save(update_fields=("slug",))


def get_email_verification_expiration() -> datetime:
    return now() + EV_EXPIRATION_TIMEDELTA


class EmailVerification(models.Model):
    code = models.CharField(null=True, max_length=EV_CODE_LENGTH)
    user = models.ForeignKey(to="users.User", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField(default=get_email_verification_expiration)

    objects = EmailVerificationManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("code", "user"), name="unique_code_and_email"
            )
        ]

    def __str__(self):
        return f"{self.user.email} | {self.expiration}"

    def save(self, *args, **kwargs):
        self.code = self.generate_code()
        super().save(*args, **kwargs)

    def generate_code(self) -> str:
        code = "".join(random.choice(digits) for _ in range(EV_CODE_LENGTH))
        if EmailVerification.objects.filter(code=code, user=self.user).exists():
            return self.generate_code()
        return code

    def send_verification_email(
        self, html_email_template_name: str = "email/verification_email.html"
    ) -> None:
        send_html_mail.delay(
            subject="Your email verification",
            html_email_template_name=html_email_template_name,
            recipient_list=[self.user.email],
            context={
                "username": self.user.username,
                "verification_code": self.code,
            },
        )

    def is_expired(self) -> bool:
        return self.expiration < now()
