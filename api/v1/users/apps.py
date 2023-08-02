from django.apps import AppConfig
from django.db.models.signals import pre_save


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api.v1.users"

    def ready(self):
        from api.v1.users import signals
        pre_save.connect(signals.update_slug_signal, sender="users.User")
