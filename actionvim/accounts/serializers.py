from rest_framework import serializers

from actionvim.organizations.models import Organization
from actionvim.accounts.models import User


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ["id", "name", "handle"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["user_code", "email", "full_name", "role"]


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    confirm_password = serializers.CharField()
    full_name = serializers.CharField()
    company_name = serializers.CharField()

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def clean(self):
        data = super().clean()
        del data["confirm_password"]
        return data
