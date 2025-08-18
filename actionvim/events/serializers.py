import json
from rest_framework import serializers

from actionvim.events.models import Event


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
