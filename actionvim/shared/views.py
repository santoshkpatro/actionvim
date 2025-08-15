from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework import status

# Create your views here.
from actionvim.shared.models import Setting
from actionvim.accounts.models import User
from actionvim.response import success_response, error_response
from actionvim.shared.serializers import SettingUpdateSerializer


class SettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setting
        fields = [
            "organization_name",
            "organization_contact_email",
            "organization_website",
            "maintenance_mode",
            "maintenance_message",
        ]


class SiteMetaView(APIView):
    def get(self, request, *args, **kwargs):
        data = {"is_ready": False, "meta": None}
        setting = Setting.load()
        if not setting:
            return success_response(
                data=data,
            )

        data["is_ready"] = True
        data["meta"] = SettingSerializer(setting).data

        return success_response(data)

    def patch(self, request, *args, **kwargs):
        setting = Setting.load()
        if setting is not None:
            return error_response(
                message="Denied setting update. Please contact support.",
                details="Setting updates are not allowed. Please contact support for assistance. Your activities are logged.",
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = SettingUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(
                message="Invalid data, please check your input.",
                details="The provided data is not valid. Please ensure all required fields are filled out correctly.",
                status=status.HTTP_400_BAD_REQUEST,
            )

        validated_data = serializer.validated_data
        Setting.initiate(
            organization_name=validated_data.get("organization_name"),
            organization_contact_email=validated_data.get("organization_contact_email"),
            organization_website=validated_data.get("organization_website", None),
        )

        User.objects.create_superuser(
            full_name=validated_data.get("superuser_full_name"),
            email=validated_data.get("superuser_email"),
            password=validated_data.get("superuser_password"),
        )
        return success_response(
            message="Site setup completed successfully.",
            details="Your site has been set up successfully. You can now log in with the superuser account.",
            data={
                "organization_name": validated_data.get("organization_name"),
                "contact_email": validated_data.get("contact_email"),
            },
        )
