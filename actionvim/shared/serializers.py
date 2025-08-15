from rest_framework import serializers


class SettingUpdateSerializer(serializers.Serializer):
    organization_name = serializers.CharField(max_length=128)
    organization_contact_email = serializers.EmailField(max_length=128)
    organization_website = serializers.URLField(
        max_length=128, required=False, allow_blank=True
    )

    superuser_email = serializers.EmailField(max_length=128)
    superuser_password = serializers.CharField(max_length=128, write_only=True)
    superuser_full_name = serializers.CharField(max_length=128)
