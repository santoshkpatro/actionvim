from django.db import models
from django.utils.crypto import get_random_string

from django.contrib.auth.models import AbstractBaseUser

from actionvim.shared.models import BaseModel


class Account(BaseModel, AbstractBaseUser):
    email = models.EmailField(unique=True)
    verified_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "accounts"


class User(BaseModel, AbstractBaseUser):
    class Role(models.TextChoices):
        OWNER = ("owner", "Owner")
        STAFF = ("staff", "Staff")
        INTERNAL = ("internal", "Internal")

    user_code = models.CharField(max_length=12, blank=True, unique=True)
    account = models.ForeignKey(
        "accounts.Account",
        on_delete=models.CASCADE,
        related_name="users",
        blank=True,
        null=True,
    )
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="users",
        blank=True,
        null=True,
    )
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STAFF,
    )
    email = models.EmailField()
    full_name = models.CharField(max_length=255, blank=True, null=True)
    is_admin = models.BooleanField(default=False)

    # password - Here password is repeated from Accounts just to support admin functionality of django

    USERNAME_FIELD = "user_code"
    REQUIRED_FIELDS = ["email", "full_name"]

    class Meta:
        db_table = "users"
        constraints = [
            models.UniqueConstraint(
                fields=["email", "organization"],
                name="unique_user_email_per_organization",
            ),
        ]

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.user_code = get_random_string(12).upper()
        super().save(*args, **kwargs)
