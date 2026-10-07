import os
from io import StringIO
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase

from apps.app_settings.models import AppSetting
from apps.lookup.models import AssetVariant, Orientation, RecordStatus, Tag


class SeedDataCommandTests(TestCase):
    def test_seed_data_is_idempotent_and_updates_existing_codes(self):
        call_command("seed_data", stdout=StringIO())
        Orientation.objects.filter(code="portrait").update(label="Changed")
        call_command("seed_data", stdout=StringIO())

        self.assertEqual(AppSetting.objects.filter(slug="ai_photo_infinity").count(), 1)
        self.assertEqual(Orientation.objects.filter(code="portrait").count(), 1)
        self.assertEqual(Orientation.objects.get(code="portrait").label, "Portrait")
        self.assertEqual(RecordStatus.objects.count(), 2)
        self.assertEqual(AssetVariant.objects.count(), 10)
        self.assertEqual(Tag.objects.count(), 6)


class EnsureSuperuserCommandTests(TestCase):
    def test_ensure_superuser_is_idempotent(self):
        with patch.dict(os.environ, {"ADMIN_EMAIL": "admin@example.test", "ADMIN_PASSWORD": "test-password"}):
            call_command("ensure_superuser", stdout=StringIO())
            call_command("ensure_superuser", stdout=StringIO())

        user = get_user_model().objects.get(email="admin@example.test")
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.check_password("test-password"))
        self.assertEqual(get_user_model().objects.filter(email="admin@example.test").count(), 1)
