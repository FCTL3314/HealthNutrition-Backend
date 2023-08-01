from django.contrib import admin

from api.v1.comparisons.admin import ComparisonInlineAdmin
from api.v1.users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    exclude = ("password", "user_permissions")
    search_fields = ("username", "slug", "first_name", "last_name")
    ordering = ("username",)
    prepopulated_fields = {"slug": ("username",)}
    readonly_fields = ("email", "date_joined", "last_login")
    inlines = (ComparisonInlineAdmin,)
