from django.apps import AppConfig


class StoresConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api.v1.stores"

    def ready(self):
        from api.v1.stores import signals
