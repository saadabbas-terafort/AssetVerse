import uuid

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("An email address is required.")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        if not extra_fields["is_staff"]:
            raise ValueError("A superuser must have is_staff=True.")
        if not extra_fields["is_superuser"]:
            raise ValueError("A superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None
    email = models.EmailField(unique=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "users_user"


class PublicUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    device_id = models.CharField(max_length=255)
    app_name = models.SlugField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "users_publicuser"
        constraints = [
            models.UniqueConstraint(
                fields=("device_id", "app_name"),
                name="unique_public_user_device_per_app",
            ),
        ]
        indexes = [
            models.Index(fields=("app_name", "is_active"), name="publicuser_app_active_idx"),
        ]

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False


class PublicUserToken(models.Model):
    key = models.CharField(max_length=40, primary_key=True)
    user = models.OneToOneField(
        PublicUser,
        on_delete=models.CASCADE,
        related_name="token",
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "users_publicusertoken"