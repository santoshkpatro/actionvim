from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from actionvim.ingest.serializers import IngestSerializer
from actionvim.events.models import Event
from actionvim.applications.models import Application


@api_view(["POST"])
def ingest(request, capture_id):
    ingest_serializer = IngestSerializer(data=request.data)
    if not ingest_serializer.is_valid():
        return Response(ingest_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    application = Application.objects.filter(capture_id=capture_id).first()
    if not application:
        return Response(
            {"error": "Application with the provided capture_id does not exist."},
            status=status.HTTP_404_NOT_FOUND,
        )

    data = ingest_serializer.validated_data
    Event.objects.create(
        application=application,
        name=data.get("name"),
        properties=data.get("properties"),
        captured_at=data.get("captured_at"),
    )
    response_data = {
        "message": "Data injected successfully",
    }
    return Response(response_data, status=status.HTTP_200_OK)
