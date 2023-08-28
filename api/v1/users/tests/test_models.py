from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.core import mail
from django.utils.timezone import now
from mixer.backend.django import mixer

from api.v1.users.constants import EV_EXPIRATION
from api.v1.users.models import EmailVerification

User = get_user_model()


class TestUserModel:
    @staticmethod
    @pytest.mark.django_db
    def test_verify(unverified_user):
        unverified_user.verify()

        assert unverified_user.is_verified is True

    @staticmethod
    @pytest.mark.django_db
    def test_create_email_verification(user: User):
        verification = user.create_email_verification()
        assert EmailVerification.objects.first() == verification

    @pytest.mark.django_db
    def test_valid_email_verifications(self, user: User):
        valid_verifications = self._create_valid_verifications(user)
        self._create_not_valid_verifications(user)

        assert len(user.valid_email_verifications()) == len(valid_verifications)

    @staticmethod
    def _create_valid_verifications(user: User) -> list[EmailVerification]:
        return mixer.cycle(5).blend("users.EmailVerification", user=user)

    @staticmethod
    def _create_not_valid_verifications(user: User) -> list[EmailVerification]:
        return mixer.cycle(5).blend(
            "users.EmailVerification",
            user=user,
            expiration=now() - timedelta(seconds=EV_EXPIRATION),
        )


class TestEmailVerificationModel:
    @staticmethod
    @pytest.mark.django_db
    def test_is_expired(
        email_verification: EmailVerification,
        expired_email_verification: EmailVerification,
    ):
        assert not email_verification.is_expired()
        assert expired_email_verification.is_expired()

    @staticmethod
    @pytest.mark.django_db
    def test_send_verification_email(user: User):
        verification = user.create_email_verification()

        subject_template_name = "email/verification_email_subject.html"
        html_email_template_name = "email/verification_email.html"

        verification.send_verification_email(
            subject_template_name, html_email_template_name
        )

        assert len(mail.outbox) == 1
        email = mail.outbox[0]
        assert email.to == [user.email]


class TestEmailVerificationManager:
    @staticmethod
    @pytest.mark.django_db
    def test_last_sent(user: User):
        mixer.cycle(5).blend("users.EmailVerification", user=user)
        expected = EmailVerification.objects.latest("created_at")
        actual = EmailVerification.objects.last_sent(user.id)
        assert expected == actual


if __name__ == "__main__":
    pytest.main()
