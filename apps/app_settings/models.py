import uuid

from django.db import models


class AppSetting(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=100, unique=True)
    label = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)
    sort_order = models.SmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "app_settings_appsetting"
        ordering = ("sort_order", "label")

    def __str__(self):
        return self.label