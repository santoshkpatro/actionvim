from django.db import models
from django.utils.crypto import get_random_string
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from actionvim.shared.models import BaseModel


class UserManager(BaseUserManager):
    def create_superuser(self, email, full_name, password=None):
        if not email:
            raise ValueError("The Email field must be set")
        if not full_name:
            raise ValueError("The Full Name field must be set")

        user = self.model(
            email=self.normalize_email(email),
            full_name=full_name,
            role="superuser",
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(BaseModel, AbstractBaseUser):
    class Role(models.TextChoices):
        SUPERUSER = ("superuser", "Superuser")
        ADMIN = ("admin", "Admin")
        STAFF = ("staff", "Staff")

    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STAFF,
    )
    full_name = models.CharField(max_length=255, blank=True, null=True)
    is_mfa_enabled = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    objects = UserManager()

    class Meta:
        db_table = "users"
