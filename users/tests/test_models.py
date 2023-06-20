import os
from datetime import timedelta

import pytest
from django.conf import settings
from django.core import mail
from django.utils.timezone import now
from mixer.backend.django import mixer

from users.models import EmailVerification
from utils.tests import generate_test_image


@pytest.mark.django_db
def test_user_create_email_verification(user):
    verification = user.create_email_verification()
    assert EmailVerification.objects.filter(user=user).first() == verification


@pytest.mark.django_db
def test_user_seconds_since_last_email_verification_sending(user):
    user.create_email_verification()
    assert user.seconds_since_last_email_verification_sending() == pytest.approx(0)


@pytest.mark.django_db
def test_user_valid_email_verifications(user):
    def create_not_valid_verifications():
        mixer.cycle(5).blend("users.EmailVerification", user=user, expiration=now() - timedelta(days=2))
        mixer.cycle(5).blend("users.EmailVerification")

    valid_verifications = mixer.cycle(5).blend("users.EmailVerification", user=user)
    create_not_valid_verifications()

    assert len(user.valid_email_verifications()) == len(valid_verifications)


@pytest.mark.django_db
def test_user_verify():
    user = mixer.blend("users.User", is_verified=False)
    user.verify()

    assert user.is_verified is True


@pytest.mark.django_db
@pytest.mark.parametrize(
    "has_image",
    (
            False,
            True,
    )
)
def test_user_get_image_url(has_image):
    if has_image:
        user = mixer.blend("users.User", image=generate_test_image())
    else:
        user = mixer.blend("users.User", image=None)

    image = user.get_image_url()

    if has_image:
        assert image == user.image.url
    else:
        assert image == os.path.join(settings.STATIC_URL, "images/default_user_image.png")


@pytest.mark.django_db
@pytest.mark.parametrize(
    "is_expired",
    (
            True,
            False,
    )
)
def test_email_verification_is_expired(is_expired):
    if is_expired:
        verification = mixer.blend("users.EmailVerification", expiration=now() - timedelta(days=2))
        assert verification.is_expired()
    else:
        verification = mixer.blend("users.EmailVerification")
        assert not verification.is_expired()


@pytest.mark.django_db
def test_send_verification_email(client, user):
    verification = user.create_email_verification()

    subject_template_name = "users/email/email_verification_subject.html"
    html_email_template_name = "users/email/email_verification_content.html"
    protocol = "https"
    host = "example.com"

    verification.send_verification_email(subject_template_name, html_email_template_name, protocol, host)

    assert len(mail.outbox) == 1
    email = mail.outbox[0]
    assert email.to == [user.email]
