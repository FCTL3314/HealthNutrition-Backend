from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.core import mail
from django.utils.timezone import now
from mixer.backend.django import mixer

from api.v1.users.models import EmailVerification

User = get_user_model()


@pytest.mark.django_db
def test_user_create_email_verification(user: User):
    verification = user.create_email_verification()
    assert EmailVerification.objects.filter(user=user).first() == verification


class TestUserValidEmailVerifications:
    @pytest.mark.django_db
    def test_user_valid_email_verifications(self, user: User):
        valid_verifications = self.create_valid_verifications(user)
        self.create_not_valid_verifications()

        assert len(user.valid_email_verifications()) == len(valid_verifications)

    @staticmethod
    def create_valid_verifications(user: User) -> list[EmailVerification]:
        return mixer.cycle(5).blend("users.EmailVerification", user=user)

    @staticmethod
    def create_not_valid_verifications() -> None:
        mixer.cycle(5).blend(
            "users.EmailVerification", expiration=now() - timedelta(days=2)
        )
        mixer.cycle(5).blend("users.EmailVerification")


@pytest.mark.django_db
def test_user_verify():
    user = mixer.blend("users.User", is_verified=False)
    user.verify()

    assert user.is_verified is True


@pytest.mark.django_db
def test_email_verification_is_expired():
    valid_verification = mixer.blend("users.EmailVerification")
    expired_verification = mixer.blend(
        "users.EmailVerification",
        expiration=now() - timedelta(days=2),
    )
    assert not valid_verification.is_expired()
    assert expired_verification.is_expired()


@pytest.mark.django_db
def test_send_verification_email(user: User):
    verification = user.create_email_verification()

    subject_template_name = "email/email_verification_subject.html"
    html_email_template_name = "email/email_verification.html"

    verification.send_verification_email(
        subject_template_name, html_email_template_name
    )

    assert len(mail.outbox) == 1
    email = mail.outbox[0]
    assert email.to == [user.email]
