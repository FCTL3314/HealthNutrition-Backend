from django.contrib import admin

from api.v1.comparisons.models import Comparison, ComparisonGroup


class ComparisonGroupInlineAdmin(admin.TabularInline):
    model = ComparisonGroup


class ComparisonInlineAdmin(admin.TabularInline):
    model = Comparison
