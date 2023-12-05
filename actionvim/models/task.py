from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from actionvim.models import BaseUUIDTimestampModel


class Task(BaseUUIDTimestampModel):
    project = models.ForeignKey(
        "Project", on_delete=models.CASCADE, related_name="project_tasks"
    )
    section = models.ForeignKey(
        "Section", on_delete=models.CASCADE, related_name="tasks"
    )
    public_id = models.CharField(max_length=20, blank=True, editable=False)
    title = models.TextField()
    description = models.TextField(blank=True, null=True)
    due_date = models.DateTimeField(blank=True, null=True)
    position = models.IntegerField(blank=True, null=True)

    archived_position = models.IntegerField(blank=True, null=True)
    archived_at = models.DateTimeField(blank=True, null=True)

    members = models.ManyToManyField("User", through="TaskMember")

    class Meta:
        db_table = "tasks"
        unique_together = ["project", "public_id"]

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if self._state.adding:
            if not self.public_id:
                project = self.project
                self.public_id = f"{project.task_prefix}-{project.task_count + 1}"
        return super().save(*args, **kwargs)

    @receiver(post_save, sender="actionvim.Task")
    def increment_project_task_count(sender, instance, created, **kwargs):
        if created:
            project = instance.project
            project.task_count += 1
            project.save(update_fields=["task_count"])

    @receiver(post_delete, sender="actionvim.Task")
    def decrement_project_task_count(sender, instance, **kwargs):
        project = instance.project
        project.task_count -= 1
        project.save(update_fields=["task_count"])
