from django.db import models
from actionvim.models.base import BaseUUIDTimestampModel


class Section(BaseUUIDTimestampModel):
    project = models.ForeignKey(
        "Project", on_delete=models.CASCADE, related_name="sections"
    )
    title = models.CharField(max_length=255)
    position = models.IntegerField(blank=True, null=True)

    archived_position = models.IntegerField(blank=True, null=True)
    archived_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "sections"

    def __str__(self) -> str:
        return self.title
