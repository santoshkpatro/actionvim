from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from actionvim.response import success_response, error_response
from actionvim.events.models import Event
from actionvim.events.serializers import EventSerializer, EventQuerySerializer


class EventViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        application_id = kwargs.get("application_id")

        query_serializer = EventQuerySerializer(data=request.query_params)
        if not query_serializer.is_valid():
            return error_response(
                message="Invalid filter parameters.",
                details="Please check for correct filter parameters.",
                error="invalid_query_parameters",
            )

        query = query_serializer.validated_data
        event_queryset = Event.objects.filter(application_id=application_id)

        if query.get("start"):
            print(query.get("start"))
            event_queryset = event_queryset.filter(captured_at__gte=query.get("start"))

        if query.get("end"):
            print(query.get("end"))
            event_queryset = event_queryset.filter(captured_at__lte=query.get("end"))

        events = event_queryset.order_by("-captured_at")[:1000]
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
