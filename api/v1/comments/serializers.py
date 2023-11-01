from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from api.v1.comments.models import Comment
from api.v1.users.serializers import UserSerializer


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    has_replies = serializers.SerializerMethodField(read_only=True)
    replies_count = serializers.IntegerField(
        source="get_descendant_count", read_only=True
    )
    parent_id = serializers.PrimaryKeyRelatedField(
        queryset=Comment.objects.all(),
        source="parent",
        allow_null=True,
        required=False,
    )
    object_id = serializers.IntegerField(write_only=True)
    content_type_id = serializers.PrimaryKeyRelatedField(
        queryset=ContentType.objects.all(),
        source="content_type",
    )

    @staticmethod
    def get_has_replies(obj: Comment) -> bool:
        return not obj.is_leaf_node()

    class Meta:
        model = Comment
        fields = (
            "id",
            "author",
            "text",
            "created_at",
            "edited",
            "parent_id",
            "has_replies",
            "replies_count",
            "object_id",
            "content_type_id",
        )
        read_only_fields = ("created_at", "edited")
