from rest_framework import serializers

from api.v1.stores.models import Store


class StoreModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ("id", "name", "url", "logo", "description", "views", "slug")
        read_only_fields = ("views", "slug")
