import django_filters

from api.v1.comments.models import Comment


class CommentFilter(django_filters.FilterSet):
    content_type_id = django_filters.NumberFilter(required=True)
    object_id = django_filters.NumberFilter(required=True)

    class Meta:
        model = Comment
        fields = ("content_type_id", "object_id")
