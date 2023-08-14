from django.db import models


class EmailVerificationManager(models.Manager):
    def last_sent(self, user_id: int):
        queryset = self.filter(user_id=user_id)
        if queryset:
            return queryset.latest("created_at")