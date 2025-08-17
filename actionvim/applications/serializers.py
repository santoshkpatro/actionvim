from rest_framework import serializers
from actionvim.applications.models import Application


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = [
            "id",
            "name",
            "description",
            "website",
            "created_at",
        ]
