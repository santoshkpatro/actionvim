from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import serializers

# Create your views here.
from actionvim.shared.models import Setting
from actionvim.response import success_response


class SettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setting
        fields = [
            "organization_name",
            "contact_email",
            "maintenance_mode",
            "maintenance_message",
        ]


class SiteMetaView(APIView):
    def get(self, request, *args, **kwargs):
        data = {"is_ready": False, "meta": None}

        try:
            setting = Setting.load()
            serializer = SettingSerializer(setting)
            data["is_ready"] = True
            data["meta"] = serializer.data
        except ValueError as e:
            pass
            # Pending Ready

        return success_response(data)
