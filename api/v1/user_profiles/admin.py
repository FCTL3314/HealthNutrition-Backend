from django.contrib import admin

from api.v1.user_profiles.models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    search_fields = ("about", "body_weight")
