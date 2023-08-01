from rest_framework import serializers

from stores.models import Store


class StoreModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ("id", "name", "url", "logo", "description", "views", "slug")
        read_only_fields = ("views", "slug")
