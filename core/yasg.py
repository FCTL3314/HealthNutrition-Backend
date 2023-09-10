from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title="Store Tracker",
        default_version="v1",
        description=(
            "Django / DRF based application for comparing prices "
            "between different stores."
        ),
        contact=openapi.Contact(email="solovev.nikita.05@gmail.com"),
        license=openapi.License(name="Apache 2.0"),
    ),
    public=True,
)

urlpatterns = [
    path(
        "docs/",
        schema_view.with_ui("swagger"),  # type: ignore
        name="swagger-schema-ui",
    ),
]
