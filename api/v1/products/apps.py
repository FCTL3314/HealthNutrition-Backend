from django.apps import AppConfig


class ProductsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api.v1.products"

    def ready(self):
        from api.v1.products import signals
