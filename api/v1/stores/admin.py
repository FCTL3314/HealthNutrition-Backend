from django.contrib import admin

from api.v1.comments.admin import CommentInlineAdmin
from api.v1.stores.models import Store


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    search_fields = ("name", "slug")
    ordering = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    inlines = (CommentInlineAdmin,)
