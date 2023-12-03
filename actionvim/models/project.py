from django.db import models
from django.utils.text import slugify

from actionvim.models.base import BaseUUIDTimestampModel


class Project(BaseUUIDTimestampModel):
    title = models.CharField(max_length=255)
    public_id = models.CharField(max_length=255, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    is_public = models.BooleanField(default=False)
    task_prefix = models.CharField(blank=True, max_length=20, null=True)
    task_count = models.IntegerField(default=0, editable=False)

    created_by = models.ForeignKey(
        "User", on_delete=models.SET_NULL, null=True, related_name="created_projects"
    )
    archived_at = models.DateTimeField(blank=True, null=True)

    users = models.ManyToManyField("User", through="Permission")

    class Meta:
        db_table = "projects"

    def __str__(self) -> str:
        return self.public_id

    def save(self, *args, **kwargs):
        if self._state.adding:
            if not self.public_id:
                self.public_id = slugify(self.title)

            if not self.task_prefix:
                self.task_prefix = "".join(
                    word[0].upper() for word in slugify(self.title).split("-")
                )
        return super().save(*args, **kwargs)
