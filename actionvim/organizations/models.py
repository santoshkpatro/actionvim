from django.db import models
from django.utils.text import slugify

from actionvim.shared.models import BaseModel


class Organization(BaseModel):
    name = models.CharField(max_length=255)
    handle = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "organizations"

    def save(self, *args, **kwargs):
        if self._state.adding:
            if not self.handle:
                self.handle = slugify(self.name)
        return super().save(*args, **kwargs)
