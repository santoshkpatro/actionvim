import uuid
from django.db import models
from django.conf import settings


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Setting(models.Model):
    # Singleton model for application settings
    organization_name = models.CharField(max_length=128)
    contact_email = models.EmailField(max_length=128)

    maintenance_mode = models.BooleanField(default=False)
    maintenance_message = models.TextField(blank=True, null=True)

    SETTING_ID = settings.SETTING_ID

    class Meta:
        db_table = "setting"

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.pk = self.SETTING_ID
        return super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        """
        Load the singleton setting instance.
        If it doesn't exist, create it with default values.
        """
        setting = cls.objects.filter(pk=cls.SETTING_ID).first()
        if not setting:
            raise ValueError(
                "Settings instance does not exist. Please create it first."
            )
