from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from actionvim.response import success_response, error_response
from actionvim.events.models import Event
from actionvim.events.serializers import EventSerializer


class EventViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        application_id = kwargs.get("application_id")
        events = Event.objects.filter(application_id=application_id)[:1000]
        serializer = EventSerializer(events, many=True)
        return success_response(data=serializer.data)

    @action(detail=False, methods=["get"])
    def schema(self, request, *args, **kwargs):
        application_id = kwargs.get("application_id")
        event_names = (
            Event.objects.filter(application_id=application_id)
            .values_list("name", flat=True)
            .distinct()
        )
        response_data = {
            "event_names": list(event_names),
        }
        return success_response(data=response_data)
