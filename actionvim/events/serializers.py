import json
from rest_framework import serializers

from actionvim.events.models import Event


class EventQuerySerializer(serializers.Serializer):
    start = serializers.DateTimeField(required=False, allow_null=True)
    end = serializers.DateTimeField(required=False, allow_null=True)
    event_names = serializers.ListField(
        child=serializers.CharField(), required=False, allow_empty=True
    )


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "id",
            "name",
            "properties",
            "source",
            "captured_at",
            "created_at",
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Convert properties to JSON string if it's a dict
        if isinstance(representation["properties"], dict):
            representation["properties"] = json.dumps(representation["properties"])
        return representation
