from django.contrib import admin

from api.v1.comments.admin import CommentInlineAdmin
from api.v1.products.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ("name", "slug")
    ordering = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    inlines = (CommentInlineAdmin,)
