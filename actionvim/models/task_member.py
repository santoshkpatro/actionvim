from django.db import models

from actionvim.models import BaseUUIDTimestampModel


class TaskMember(BaseUUIDTimestampModel):
    task = models.ForeignKey(
        "Task", on_delete=models.CASCADE, related_name="task_members"
    )
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="user_task_members"
    )

    class Meta:
        db_table = "task_members"

    def __str__(self) -> str:
        return str(self.id)
