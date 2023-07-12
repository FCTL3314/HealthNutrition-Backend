from datetime import timedelta
from uuid import uuid4

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import QuerySet
from django.urls import reverse
from django.utils.timezone import now

from common.decorators import order_queryset
from common.models import SlugifyMixin
from utils.mail import convert_html_to_email_message
from utils.static import get_static_file


class User(SlugifyMixin, AbstractUser):
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

    def get_absolute_url(self):
        return reverse("users:profile", args=(self.slug,))

    def is_request_user_matching(self, request) -> bool:
        return self == request.user

    def seconds_since_last_email_verification_sending(self) -> int:
        if self.valid_email_verifications():
            last_verification = EmailVerification.objects.latest("created_at")
            elapsed_time = now() - last_verification.created_at
            return elapsed_time.seconds
        return settings.EMAIL_SENDING_SECONDS_INTERVAL + 1

    def is_verification_sending_interval_passed(self) -> bool:
        seconds_since_last_sending = self.seconds_since_last_email_verification_sending()
        return seconds_since_last_sending > settings.EMAIL_SENDING_SECONDS_INTERVAL

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
        self.is_verified = True
        if commit:
            self.save(update_fields=("is_verified",))

    def get_image_url(self) -> str:
        if self.image:
            return self.image.url
        return get_static_file("images/default_user_image.png")


class EmailVerification(models.Model):
    code = models.UUIDField(null=True, unique=True)
    user = models.ForeignKey(to="users.User", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    def __str__(self):
        return f"{self.user.email} | {self.expiration}"

    def save(self, *args, **kwargs):
        self.code = self.generate_code()
        self.expiration = now() + timedelta(hours=2)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "users:email-verification",
            kwargs={"email": self.user.email, "code": self.code},
        )

    def generate_code(self) -> uuid4:
        code = uuid4()
        if EmailVerification.objects.filter(code=code).exists():
            return self.generate_code()
        return code

    def send_verification_email(
        self,
        subject_template_name: str,
        html_email_template_name: str,
        domain: str,
    ) -> None:
        context = {
            "user": self.user,
            "verification_link": f"https://{domain}/{self.get_absolute_url()}",
        }

        msg = convert_html_to_email_message(
            subject_template_name=subject_template_name,
            html_email_template_name=html_email_template_name,
            emails_list=[self.user.email],
            context=context,
        )
        msg.send()

    def is_expired(self) -> bool:
        return self.expiration < now()
