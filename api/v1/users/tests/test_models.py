import pytest
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from mixer.backend.django import mixer

from api.v1.users.constants import EV_EXPIRATION_TIMEDELTA
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
        email_verification = EmailVerification.objects.create(user=user)
        assert EmailVerification.objects.first() == email_verification

    @staticmethod
    def _create_valid_verifications(user: User) -> list[EmailVerification]:
        return mixer.cycle(5).blend("users.EmailVerification", user=user)

    @staticmethod
    def _create_not_valid_verifications(user: User) -> list[EmailVerification]:
        return mixer.cycle(5).blend(
            "users.EmailVerification",
            user=user,
            expiration=now() - EV_EXPIRATION_TIMEDELTA,
        )


class TestEmailVerificationModel:
    @staticmethod
    @pytest.mark.django_db
    def test_is_expired(
        email_verification: EmailVerification,
        expired_email_verification: EmailVerification,
    ):
        assert not email_verification.is_expired
        assert expired_email_verification.is_expired


class TestEmailVerificationManager:
    @staticmethod
    @pytest.mark.django_db
    def test_last_sent(user: User):
        mixer.cycle(2).blend("users.EmailVerification", user=user)
        expected = EmailVerification.objects.latest("created_at")
        actual = EmailVerification.objects.last_sent(user.id)
        assert expected == actual


if __name__ == "__main__":
    pytest.main()
