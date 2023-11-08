from django.contrib import admin

from api.v1.categories.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ("name", "slug")
    ordering = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("views",)
