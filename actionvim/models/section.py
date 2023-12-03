from django.db import models
from actionvim.models.base import BaseUUIDTimestampModel


class Section(BaseUUIDTimestampModel):
    project = models.ForeignKey("Project", on_delete=models.CASCADE, related_name="project_sections")
    title = models.CharField(max_length=255)
    position = models.IntegerField(blank=True)

    class Meta:
        db_table = "sections"
        unique_together = ["project", "position"]

    def __str__(self) -> str:
        return self.title
