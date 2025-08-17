from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from actionvim.applications.serializers import (
    ApplicationSerializer,
    ApplicationCreateSerializer,
)
from actionvim.applications.models import Application, ApplicationMember
from actionvim.response import success_response, error_response


class AplicationViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        create_serializer = ApplicationCreateSerializer(data=request.data)
        if not create_serializer.is_valid():
            return error_response(
                message="Invalid data",
                details="Please check the provided data.",
                error="invalid_data",
            )
        new_application = Application(
            **create_serializer.validated_data,
        )
        new_application.save()
        ApplicationMember.objects.create(
            application=new_application,
            user=request.user,
            role=ApplicationMember.Role.ADMIN,
        )
        serializer = ApplicationSerializer(new_application)
        return success_response(
            data=serializer.data, message="Application created successfully."
        )

    def list(self, request, *args, **kwargs):
        applications = Application.objects.filter(members__user=request.user)
        serializer = ApplicationSerializer(applications, many=True)
        return success_response(serializer.data)

    @action(detail=False, methods=["get"], url_path="mine")
    def mine(self, request, *args, **kwargs):
        applications = Application.objects.filter(members__user=request.user)
        serializer = ApplicationSerializer(applications, many=True)
        return success_response(serializer.data)
