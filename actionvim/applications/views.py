from django.shortcuts import render
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated

from actionvim.applications.serializers import ApplicationSerializer
from actionvim.applications.models import Application, ApplicationMember
from actionvim.response import success_response, error_response


class AplicationViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        applications = Application.objects.filter(members__user=request.user)
        serializer = ApplicationSerializer(applications, many=True)
        return success_response(serializer.data)
