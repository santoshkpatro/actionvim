from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.db.models import Q

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

        properties = []
        i = 0
        while True:
            key = request.query_params.get(f"properties[{i}][key]")
            operator = request.query_params.get(f"properties[{i}][operator]")
            value = request.query_params.get(f"properties[{i}][value]")
            if key is None or operator is None or value is None:
                break

            properties.append(
                {
                    "key": key,
                    "operator": operator,
                    "value": value,
                }
            )
            i += 1
        query = query_serializer.validated_data
        event_queryset = Event.objects.filter(application_id=application_id)

        if query.get("start"):
            event_queryset = event_queryset.filter(captured_at__gte=query.get("start"))

        if query.get("end"):
            event_queryset = event_queryset.filter(captured_at__lte=query.get("end"))

        for property in properties:
            key = property["key"]
            operator = property["operator"]
            value = property["value"]

            if operator == "eq":
                event_queryset = event_queryset.filter(
                    Q(**{f"properties__{key}": str(value)})
                    | Q(**{f"properties__{key}": value})
                )
            elif operator == "lt":
                event_queryset = event_queryset.filter(
                    Q(**{f"properties__{key}__lt": value})
                )
            elif operator == "gt":
                event_queryset = event_queryset.filter(
                    Q(**{f"properties__{key}__gt": value})
                )
            elif operator == "neq":
                event_queryset = event_queryset.exclude(
                    Q(**{f"properties__{key}": str(value)})
                )
            elif operator == "contains":
                event_queryset = event_queryset.filter(
                    Q(**{f"properties__{key}__icontains": str(value)})
                )
            elif operator == "not_contains":
                event_queryset = event_queryset.exclude(
                    Q(**{f"properties__{key}__icontains": str(value)})
                )

        # print(f"Filtered events: {event_queryset.query}")

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
