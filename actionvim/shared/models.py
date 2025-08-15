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
    organization_contact_email = models.EmailField(max_length=128)
    organization_website = models.URLField(max_length=128, blank=True, null=True)

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
        """
        return cls.objects.filter(pk=cls.SETTING_ID).first()

    @classmethod
    def initiate(
        cls, organization_name, organization_contact_email, organization_website=None
    ):
        cls.objects.create(
            pk=cls.SETTING_ID,
            organization_name=organization_name,
            organization_contact_email=organization_contact_email,
            organization_website=organization_website,
        )
        return cls
