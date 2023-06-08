import os
from datetime import timedelta
from uuid import uuid4

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.timezone import now

from common.models import SlugifyMixin
from utils.mail import convert_html_to_email_message


class User(SlugifyMixin, AbstractUser):
    email = models.EmailField(unique=True)
    image = models.ImageField(upload_to='users', null=True, blank=True)
    slug = models.SlugField(unique=True)
    comparisons = models.ManyToManyField('products.Product', through='comparisons.Comparison', blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    def is_request_user_matching(self, request):
        return self == request.user

    def seconds_since_last_email_verification_sending(self):
        if valid_verifications := self.valid_email_verifications():
            elapsed_time = now() - valid_verifications.first().created_at
        else:
            elapsed_time = timedelta(seconds=settings.EMAIL_SEND_INTERVAL_SECONDS)
        return elapsed_time.seconds

    def create_email_verification(self):
        code = uuid4()
        while EmailVerification.objects.filter(code=code).exists():
            self.create_email_verification()
        return EmailVerification.objects.create(code=code, user=self)

    def valid_email_verifications(self):
        verifications = self.emailverification_set.filter(expiration__gt=now())
        return verifications.order_by('-created_at')

    def verify(self, commit=True):
        self.is_verified = True
        if commit:
            self.save(update_fields=('is_verified',))

    def get_image_url(self):
        return self.image.url if self.image else os.path.join(settings.STATIC_URL, 'images/default_user_image.png')


class EmailVerification(models.Model):
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField(default=now() + timedelta(hours=2))

    def __str__(self):
        return f'{self.user.email} | {self.expiration}'

    def send_verification_email(self, subject_template_name, html_email_template_name, protocol):
        link = reverse('users:email-verification', kwargs={'email': self.user.email, 'code': self.code})

        context = {
            'user': self.user,
            'protocol': protocol,
            'verification_link': settings.DOMAIN_NAME + link,
        }

        msg = convert_html_to_email_message(
            subject_template_name=subject_template_name,
            html_email_template_name=html_email_template_name,
            emails_list=[self.user.email],
            context=context,
        )
        msg.send()

    def is_expired(self):
        return self.expiration < now()
