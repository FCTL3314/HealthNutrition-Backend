from django.contrib import admin

from comparisons.models import Comparison


class ComparisonInlineAdmin(admin.TabularInline):
    model = Comparison
