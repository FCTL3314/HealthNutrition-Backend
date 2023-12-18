from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from api.v1.comments.admin import CommentInlineAdmin
from api.v1.products.models import Product


@admin.register(Product)
class ProductAdmin(SummernoteModelAdmin):
    summernote_fields = ("description",)
    search_fields = ("name", "slug")
    ordering = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    inlines = (CommentInlineAdmin,)
