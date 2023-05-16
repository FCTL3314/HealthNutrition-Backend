from django.contrib import admin

from stores.models import Store


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    search_fields = ('name', 'slug')
    ordering = ('name',)
    prepopulated_fields = {'slug': ('name',)}
