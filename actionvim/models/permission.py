from actionvim.models.base import BaseUUIDTimestampModel
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Permission(BaseUUIDTimestampModel):
    class Role(models.TextChoices):
        ADMIN = ("admin", "Admin")
        MEMBER = ("member", "Member")

    project = models.ForeignKey(
        "Project", on_delete=models.CASCADE, related_name="project_permissions"
    )
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="user_permissions"
    )
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.MEMBER)

    class Meta:
        db_table = "permissions"

    def __str__(self) -> str:
        return str(self.id)

    @receiver(post_save, sender="actionvim.Project")
    def create_poject_admin_permission(sender, instance, created, **kwargs):
        if created:
            Permission.objects.create(
                project=instance, user=instance.created_by, role="admin"
            )
