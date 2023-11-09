from rest_framework import serializers

from api.v1.comments.models import Comment
from api.v1.users.serializers import UserSerializer


class BaseCommentSerializer(serializers.ModelSerializer):
    object_id = serializers.IntegerField(required=True)
    content_type = serializers.SlugRelatedField(
        queryset=Comment.ALLOWED_CONTENT_TYPES_QUERYSET,
        slug_field="model",
        required=True,
    )
    parent_id = serializers.PrimaryKeyRelatedField(
        queryset=Comment.objects.all(),
        source="parent",
        allow_null=True,
        required=False,
    )

    class Meta:
        abstract = True
        model = Comment
        fields = (
            "parent_id",
            "object_id",
            "content_type",
        )


class CommentSerializer(BaseCommentSerializer):
    author = UserSerializer(read_only=True)

    class Meta(BaseCommentSerializer.Meta):
        fields = BaseCommentSerializer.Meta.fields + (
            "id",
            "text",
            "author",
            "is_edited",
        )


class DetailedCommentSerializer(CommentSerializer):
    parent = CommentSerializer(read_only=True)
    has_replies = serializers.SerializerMethodField(read_only=True)
    replies_count = serializers.IntegerField(
        source="get_descendant_count", read_only=True
    )

    @staticmethod
    def get_has_replies(obj: Comment) -> bool:
        return not obj.is_leaf_node()

    class Meta(BaseCommentSerializer.Meta):
        fields = CommentSerializer.Meta.fields + (
            "parent",
            "created_at",
            "has_replies",
            "replies_count",
        )
        read_only_fields = ("created_at", "is_edited")


class CommentReadSerializer(BaseCommentSerializer):
    ...
