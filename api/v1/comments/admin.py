from django.contrib.contenttypes.admin import GenericTabularInline

from api.v1.comments.models import Comment


class CommentInlineAdmin(GenericTabularInline):
    model = Comment
    ordering = ("-created_at",)
