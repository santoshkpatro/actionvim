from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from actionvim.models.base import BaseUUIDTimestampModel


class UserManager(BaseUserManager):
    def create_user(self, username, email, first_name, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            first_name=first_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, first_name, password=None):
        user = self.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
        )
        user.role = "admin"
        user.save(using=self._db)
        return user


class User(BaseUUIDTimestampModel, AbstractBaseUser):
    class Role(models.TextChoices):
        BASIC = ("basic", "Basic")
        ADMIN = ("admin", "Admin")

    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=25, blank=True, null=True)
    avatar = models.ImageField(blank=True, null=True, upload_to="avatars/")

    is_password_expired = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    email_verified_at = models.DateTimeField(blank=True, null=True)
    phone_verified_at = models.DateTimeField(blank=True, null=True)

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.BASIC)

    last_login_at = models.DateTimeField(blank=True, null=True)
    last_login_ip = models.GenericIPAddressField(blank=True, null=True)

    projects = models.ManyToManyField("Project", through="Permission")

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "first_name"]

    class Meta:
        db_table = "users"

    def __str__(self) -> str:
        return self.username

    # Django Admin Methods
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.role == self.Role.ADMIN
    
    @property
    def tokens(self):
        return {
            "access": str(AccessToken.for_user(self)),
            "refresh": str(RefreshToken.for_user(self))
        }
