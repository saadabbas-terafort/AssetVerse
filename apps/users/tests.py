import json

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from apps.app_settings.models import AppSetting
from apps.category.models import Category
from apps.lookup.models import AssetVariant, Orientation, RecordStatus, Tag


class DeviceAuthApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.app = AppSetting.objects.create(
            slug="ai_photo_infinity",
            label="AI Photo Editor Infinity",
            is_active=True,
            sort_order=1,
        )

    def test_health_endpoint_returns_envelope(self):
        response = self.client.get("/health/")
        payload = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(payload["status"], 200)
        self.assertEqual(payload["data"], {})
        self.assertEqual(payload["message"], "Success")

    def test_device_auth_registers_public_user_and_token(self):
        response = self.client.post(
            "/api/users/auth/",
            {"device_id": "phone-123"},
            format="json",
            HTTP_X_APP_NAME="ai_photo_infinity",
        )
        payload = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(payload["status"], 200)
        self.assertEqual(payload["data"]["user"]["device_id"], "phone-123")
        self.assertEqual(payload["data"]["user"]["app_name"], "ai_photo_infinity")
        self.assertTrue(payload["data"]["token"])

    def test_second_device_login_rotates_token_and_old_token_is_rejected(self):
        first = self.client.post(
            "/api/users/auth/", {"device_id": "rotate-device"}, format="json", HTTP_X_APP_NAME="ai_photo_infinity"
        )
        first_token = json.loads(first.content)["data"]["token"]
        second = self.client.post(
            "/api/users/auth/", {"device_id": "rotate-device"}, format="json", HTTP_X_APP_NAME="ai_photo_infinity"
        )
        second_payload = json.loads(second.content)
        second_token = second_payload["data"]["token"]

        self.assertNotEqual(first_token, second_token)
        self.assertEqual(second_payload["message"], "User logged in successfully")
        rejected = self.client.get(
            "/api/lookups/",
            HTTP_AUTHORIZATION=f"PublicToken {first_token}",
            HTTP_X_APP_NAME="ai_photo_infinity",
        )
        self.assertEqual(rejected.status_code, 401)

    def test_public_token_is_rejected_for_a_different_app_header(self):
        AppSetting.objects.create(slug="other_app", label="Other App", is_active=True, sort_order=2)
        auth_response = self.client.post(
            "/api/users/auth/", {"device_id": "scoped-device"}, format="json", HTTP_X_APP_NAME="ai_photo_infinity"
        )
        token = json.loads(auth_response.content)["data"]["token"]

        response = self.client.get(
            "/api/lookups/",
            HTTP_AUTHORIZATION=f"PublicToken {token}",
            HTTP_X_APP_NAME="other_app",
        )
        self.assertEqual(response.status_code, 401)

    @override_settings(PUBLIC_API_KEY="test-key")
    def test_category_list_requires_api_key_and_app_name(self):
        response = self.client.get("/api/categories/")
        self.assertEqual(response.status_code, 403)

    @override_settings(PUBLIC_API_KEY="test-key")
    def test_category_list_returns_active_rows_for_the_app(self):
        status = RecordStatus.objects.create(code="active", label="Active", sort_order=1, is_active=True)
        orientation = Orientation.objects.create(code="portrait", label="Portrait", sort_order=1, is_active=True)
        availability = Tag.objects.create(
            code="free",
            label="Free",
            sort_order=1,
            is_active=True,
            tag_type=Tag.TagType.AVAILABILITY,
        )
        section = Tag.objects.create(
            code="home_listing",
            label="Home Listing",
            sort_order=1,
            is_active=True,
            tag_type=Tag.TagType.LISTING,
        )
        variant = AssetVariant.objects.create(
            code="frame",
            label="Frame",
            sort_order=1,
            is_active=True,
        )
        category = Category.objects.create(
            app=self.app,
            title="Home",
            actionbar="",
            cover_image=SimpleUploadedFile("cover.jpg", b"x", content_type="image/jpeg"),
            orientation=orientation,
            tag=availability,
            section=section,
            status=status,
            variant=variant,
            api_option="",
            sort_order=1,
        )
        other_app = AppSetting.objects.create(
            slug="other_app",
            label="Other App",
            is_active=True,
            sort_order=2,
        )
        inactive_status = RecordStatus.objects.create(
            code="inactive",
            label="Inactive",
            sort_order=2,
            is_active=True,
        )
        Category.objects.create(
            app=other_app,
            title="Other app category",
            actionbar="",
            cover_image=SimpleUploadedFile("other.jpg", b"x", content_type="image/jpeg"),
            orientation=orientation,
            tag=availability,
            section=section,
            status=status,
            variant=variant,
            api_option="",
            sort_order=2,
        )
        Category.objects.create(
            app=self.app,
            title="Inactive category",
            actionbar="",
            cover_image=SimpleUploadedFile("inactive.jpg", b"x", content_type="image/jpeg"),
            orientation=orientation,
            tag=availability,
            section=section,
            status=inactive_status,
            variant=variant,
            api_option="",
            sort_order=3,
        )

        response = self.client.get(
            "/api/categories/",
            HTTP_X_API_KEY="test-key",
            HTTP_X_APP_NAME="ai_photo_infinity",
        )
        payload = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(payload["data"]), 1)
        self.assertEqual(payload["data"][0]["title"], category.title)

    def test_lookup_bundle_rejects_anonymous_request(self):
        response = self.client.get("/api/lookups/")

        self.assertEqual(response.status_code, 401)

    @override_settings(PUBLIC_API_KEY="test-key")
    def test_tag_endpoint_does_not_require_app_header(self):
        response = self.client.get("/api/lookups/tags/", HTTP_X_API_KEY="test-key")

        self.assertEqual(response.status_code, 200)

    @override_settings(PUBLIC_API_KEY="test-key")
    def test_lookup_bundle_returns_active_lookups(self):
        RecordStatus.objects.create(code="active", label="Active", sort_order=1, is_active=True)
        RecordStatus.objects.create(code="hidden", label="Hidden", sort_order=2, is_active=False)
        Tag.objects.create(code="free", label="Free", sort_order=1, is_active=True, tag_type=Tag.TagType.AVAILABILITY)
        Tag.objects.create(code="listing", label="Listing", sort_order=2, is_active=True, tag_type=Tag.TagType.LISTING)
        auth_response = self.client.post(
            "/api/users/auth/",
            {"device_id": "lookup-device"},
            format="json",
            HTTP_X_APP_NAME="ai_photo_infinity",
        )
        token = json.loads(auth_response.content)["data"]["token"]
        response = self.client.get(
            "/api/lookups/",
            HTTP_AUTHORIZATION=f"PublicToken {token}",
            HTTP_X_APP_NAME="ai_photo_infinity",
        )
        payload = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            set(payload["data"]),
            {
                "orientations", "tags", "sections", "screen_tags", "variant_tags", "hashtags", "locales",
                "statuses", "variants", "frame_keys", "frame_types", "effect_types", "slide_types",
            },
        )
        self.assertEqual([row["code"] for row in payload["data"]["tags"]], ["free"])
        self.assertEqual([row["code"] for row in payload["data"]["sections"]], ["listing"])
        self.assertNotIn("hidden", [row["code"] for row in payload["data"]["statuses"]])

    @override_settings(PUBLIC_API_KEY="test-key")
    def test_public_catalog_write_returns_405_envelope(self):
        response = self.client.post(
            "/api/categories/",
            {},
            format="json",
            HTTP_X_API_KEY="test-key",
            HTTP_X_APP_NAME="ai_photo_infinity",
        )

        payload = json.loads(response.content)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(payload["status"], 405)
        self.assertEqual(payload["data"], {})
        self.assertIn("message", payload)

    @override_settings(DEBUG=False)
    def test_unknown_api_route_returns_json_error_envelope(self):
        response = self.client.get("/api/not-a-route/")
        payload = json.loads(response.content)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(payload["status"], 404)
        self.assertEqual(payload["data"], {})
        self.assertIn("message", payload)


class CategoryAdminApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.app = AppSetting.objects.create(
            slug="ai_photo_infinity",
            label="AI Photo Editor Infinity",
            is_active=True,
            sort_order=1,
        )
        self.staff = get_user_model().objects.create_user(
            email="staff@example.test",
            password="test-password",
            is_staff=True,
        )
        self.token = Token.objects.create(user=self.staff)
        Orientation.objects.create(code="portrait", label="Portrait", sort_order=1, is_active=True)
        RecordStatus.objects.create(code="active", label="Active", sort_order=1, is_active=True)
        AssetVariant.objects.create(code="frame", label="Frame", sort_order=1, is_active=True)
        Tag.objects.create(
            code="free", label="Free", sort_order=1, is_active=True, tag_type=Tag.TagType.AVAILABILITY
        )
        Tag.objects.create(
            code="home_listing", label="Home Listing", sort_order=1, is_active=True, tag_type=Tag.TagType.LISTING
        )

    def test_staff_can_create_category_using_slug_and_lookup_codes(self):
        from io import BytesIO
        from PIL import Image

        image_buffer = BytesIO()
        Image.new("RGB", (1, 1), color="white").save(image_buffer, format="PNG")
        response = self.client.post(
            "/api/categories/admin/",
            {
                "app": "ai_photo_infinity",
                "title": "Home",
                "actionbar": "",
                "cover_image": SimpleUploadedFile("cover.png", image_buffer.getvalue(), content_type="image/png"),
                "orientation": "portrait",
                "tag": "free",
                "section": "home_listing",
                "status": "active",
                "variant": "frame",
                "api_option": "plain text",
                "sort_order": 1,
            },
            format="multipart",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )

        payload = json.loads(response.content)
        self.assertEqual(response.status_code, 201, payload)
        self.assertEqual(payload["status"], 201)
        self.assertEqual(payload["data"]["app"], {"slug": "ai_photo_infinity", "label": "AI Photo Editor Infinity"})
        self.assertEqual(payload["data"]["orientation"], {"code": "portrait", "label": "Portrait"})
        self.assertEqual(payload["data"]["tag"], {"code": "free", "label": "Free"})
        self.assertTrue(payload["data"]["cover_image"].startswith("http://testserver/"))

        category_id = payload["data"]["id"]
        update_response = self.client.patch(
            f"/api/categories/admin/{category_id}/",
            {"api_option": "updated"},
            format="json",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(json.loads(update_response.content)["data"]["api_option"], "updated")

        delete_response = self.client.delete(
            f"/api/categories/admin/{category_id}/",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )
        self.assertEqual(delete_response.status_code, 200)
        self.assertEqual(json.loads(delete_response.content)["data"], {})

    def test_non_staff_token_cannot_access_admin_json_routes(self):
        non_staff = get_user_model().objects.create_user(email="user@example.test", password="test-password")
        token = Token.objects.create(user=non_staff)
        response = self.client.get(
            "/api/categories/admin/",
            HTTP_AUTHORIZATION=f"Token {token.key}",
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(json.loads(response.content)["data"], {})

    def test_admin_category_write_rejects_unknown_lookup_code_in_envelope(self):
        response = self.client.post(
            "/api/categories/admin/",
            {"orientation": "unknown"},
            format="json",
            HTTP_AUTHORIZATION=f"Token {self.token.key}",
        )

        payload = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(payload["status"], 400)
        self.assertEqual(payload["data"], {})
        self.assertIn("message", payload)
