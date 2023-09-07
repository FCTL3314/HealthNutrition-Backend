from django.contrib import admin

from api.v1.comments.models import ProductComment, StoreComment


class BaseCommentAdmin(admin.TabularInline):
    search_fields = ("text",)
    ordering = ("created_at",)


class ProductCommentAdmin(BaseCommentAdmin):
    model = ProductComment


class StoreCommentAdmin(BaseCommentAdmin):
    model = StoreComment
