import django_filters

from api.v1.comments.models import ProductComment, StoreComment


class ProductCommentFilter(django_filters.FilterSet):
    product_id = django_filters.NumberFilter(required=True)

    class Meta:
        model = ProductComment
        fields = ("product_id",)


class StoreCommentFilter(django_filters.FilterSet):
    store_id = django_filters.NumberFilter(required=True)

    class Meta:
        model = StoreComment
        fields = ("store_id",)
