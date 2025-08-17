from rest_framework import serializers


class IngestSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=128)
    properties = serializers.JSONField(default=dict)
    captured_at = serializers.DateTimeField()
