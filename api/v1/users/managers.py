from django.db import models


class EmailVerificationQuerySet(models.QuerySet):
    def last_sent(self, user_id: int):
        if queryset := self.filter(user_id=user_id):
            return queryset.latest("created_at")


class EmailVerificationManager(models.Manager.from_queryset(EmailVerificationQuerySet)):
    ...
