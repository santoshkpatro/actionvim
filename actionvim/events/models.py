from django.db import models
from django.utils import timezone

from actionvim.shared.models import BaseModel


class Event(BaseModel):
    application = models.ForeignKey(
        "applications.Application", on_delete=models.CASCADE, related_name="events"
    )
    name = models.CharField(max_length=128, db_index=True)
    properties = models.JSONField(default=dict, blank=True)
    source = models.CharField(max_length=64, default="web")
    captured_at = models.DateTimeField(default=timezone.now, blank=True, db_index=True)

    class Meta:
        db_table = "events"
