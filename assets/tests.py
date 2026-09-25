from django.test import TestCase

# Create your tests here.

from .factories import AppFactory


class AppTest(TestCase):

    def test_create_app(self):
        app = AppFactory()

        self.assertEqual(app.slug, "app-1")
        self.assertEqual(app.lable, "App 1")
        self.assertEqual(app.sortorder, 1)

        self.assertIsNotNone(app.status)
        self.assertEqual(app.status.lable, "Status 1")
        self.assertEqual(app.status.code, "STATUS_1")
        self.assertTrue(app.status.is_active)

        self.assertIsNotNone(app.created_at)
        self.assertIsNotNone(app.update_at)

    def test_app_str(self):
        app = AppFactory()

        self.assertEqual(str(app), app.lable)

