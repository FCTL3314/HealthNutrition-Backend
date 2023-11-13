from django.contrib import admin

from api.v1.diets.models import DietType, Diet, DietProduct


class DietProductAdmin(admin.TabularInline):
    model = DietProduct


@admin.register(DietType)
class DietTypeAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Diet)
class DietAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    ordering = ("name",)
    inlines = (DietProductAdmin,)
