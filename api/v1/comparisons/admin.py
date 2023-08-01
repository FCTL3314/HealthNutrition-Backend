from django.contrib import admin

from api.v1.comparisons.models import Comparison


class ComparisonInlineAdmin(admin.TabularInline):
    model = Comparison
