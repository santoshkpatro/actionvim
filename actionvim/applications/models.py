from django.db import models
from django.conf import settings
from django.utils.crypto import get_random_string

from actionvim.shared.models import BaseModel


class Application(BaseModel):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    capture_id = models.CharField(max_length=32, blank=True, unique=True)

    class Meta:
        db_table = "applications"

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.capture_id = "cap_" + get_random_string(28).lower()
        return super().save(*args, **kwargs)


class ApplicationMember(BaseModel):
    class Role(models.TextChoices):
        ADMIN = ("admin", "Admin")
        MEMBER = ("member", "Member")

    application = models.ForeignKey(
        "applications.Application", on_delete=models.CASCADE, related_name="members"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="application_members",
    )
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.MEMBER)

    class Meta:
        db_table = "application_members"
        constraints = [
            models.UniqueConstraint(
                fields=["application", "user"], name="unique_application_member"
            )
        ]
