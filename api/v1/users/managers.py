from django.db import models


class EmailVerificationManager(models.Manager):
    def last_sent(self, user):
        return self.filter(user=user).latest("created_at")
