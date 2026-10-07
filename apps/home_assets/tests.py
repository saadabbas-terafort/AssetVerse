import json

from django.test import TestCase, override_settings
from rest_framework.test import APIClient

from apps.app_settings.models import AppSetting
from apps.category.models import Category
from apps.effects.models import Effect
from apps.fonts.models import Font
from apps.home_assets.models import Frame, FrameAsset, FrameConstraint
from apps.home_assets.serializers import FrameSerializer
from apps.lookup.models import (
    AssetVariant,
    EffectType,
    FrameKey,
    FrameType,
    Orientation,
    RecordStatus,
    SlideType,
    Tag,
)
from apps.slides.models import Slide
from apps.stickers.models import Sticker


class CatalogScopingTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.app = AppSetting.objects.create(slug="app_a", label="App A", sort_order=1, is_active=True)
        self.other_app = AppSetting.objects.create(slug="app_b", label="App B", sort_order=2, is_active=True)
        self.active = RecordStatus.objects.create(code="active", label="Active", sort_order=1, is_active=True)
        self.inactive = RecordStatus.objects.create(code="inactive", label="Inactive", sort_order=2, is_active=True)
        self.orientation = Orientation.objects.create(code="portrait", label="Portrait", sort_order=1, is_active=True)
        self.availability = Tag.objects.create(
            code="free", label="Free", sort_order=1, is_active=True, tag_type=Tag.TagType.AVAILABILITY
        )
        self.frame_variant = AssetVariant.objects.create(code="frame", label="Frame", sort_order=1, is_active=True)
        self.effect_variant = AssetVariant.objects.create(code="effect", label="Effect", sort_order=2, is_active=True)
        self.frame_type = FrameType.objects.create(code="frame", label="Frame", sort_order=1, is_active=True)
        self.effect_type = EffectType.objects.create(code="filter", label="Filter", sort_order=1, is_active=True)
        self.frame_key = FrameKey.objects.create(code="cover", label="Cover", sort_order=1, is_active=True)
        self.root = self.make_category(self.app, "root", None, self.frame_variant, self.active)
        self.frame_category = self.make_category(self.app, "frames", self.root, self.frame_variant, self.active)
        self.effect_root = self.make_category(self.app, "effect root", None, self.effect_variant, self.active)
        self.effect_category = self.make_category(self.app, "effects", self.effect_root, self.effect_variant, self.inactive)
        self.other_root = self.make_category(self.other_app, "other root", None, self.effect_variant, self.active)
        self.other_category = self.make_category(self.other_app, "other effects", self.other_root, self.effect_variant, self.active)

    def make_category(self, app, title, parent, variant, status):
        return Category.objects.create(
            app=app,
            title=title,
            actionbar="",
            cover_image="cover.jpg",
            parent=parent,
            orientation=self.orientation,
            tag=self.availability,
            status=status,
            variant=variant,
            api_option="",
            sort_order=1,
        )

    @override_settings(PUBLIC_API_KEY="test-key")
    def test_effect_list_scopes_by_app_and_asset_status_only(self):
        own_active = Effect.objects.create(
            title="Own active",
            effect="own",
            category=self.effect_category,
            effect_type=self.effect_type,
            cover="cover.png",
            file="effect.bin",
            status=self.active,
            sort_order=1,
        )
        Effect.objects.create(
            title="Other app",
            effect="other",
            category=self.other_category,
            effect_type=self.effect_type,
            cover="cover.png",
            file="effect.bin",
            status=self.active,
            sort_order=2,
        )
        Effect.objects.create(
            title="Inactive asset",
            effect="inactive",
            category=self.effect_category,
            effect_type=self.effect_type,
            cover="cover.png",
            file="effect.bin",
            status=self.inactive,
            sort_order=3,
        )

        response = self.client.get(
            "/api/effects/?category=" + str(self.effect_category.pk) + "&effect_type=filter",
            HTTP_X_API_KEY="test-key",
            HTTP_X_APP_NAME="app_a",
        )
        payload = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual([row["id"] for row in payload["data"]], [str(own_active.pk)])
        self.assertEqual(payload["data"][0]["effect_type"], "filter")

    @override_settings(PUBLIC_API_KEY="test-key")
    def test_active_frame_read_includes_constraints_and_inactive_layers(self):
        frame = Frame.objects.create(
            title="Layered frame",
            category=self.frame_category,
            frame_type=self.frame_type,
            editor="frames",
            ratio_width="1.00",
            ratio_height="1.00",
            status=self.active,
            image_picker=True,
            sort_order=1,
        )
        frame.tags.add(self.availability)
        FrameConstraint.objects.create(
            frame=frame,
            value_1="0.1000",
            value_2="0.2000",
            value_3="0.3000",
            value_4="0.4000",
            sort_order=1,
        )
        layer = FrameAsset.objects.create(
            frame=frame,
            key=self.frame_key,
            image="layer.png",
            status=self.inactive,
            sort_order=1,
        )

        response = self.client.get(
            f"/api/home-assets/frames/{frame.pk}/",
            HTTP_X_API_KEY="test-key",
            HTTP_X_APP_NAME="app_a",
        )
        payload = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(payload["data"]["constraints"][0]["value_1"], "0.1000")
        self.assertEqual(payload["data"]["tags"], ["free"])
        self.assertEqual(payload["data"]["assets"][0]["key"], "cover")
        self.assertEqual(payload["data"]["assets"][0]["status"], "inactive")
        self.assertEqual(payload["data"]["assets"][0]["image"], f"http://testserver/media/{layer.image}")

    def test_frame_write_rejects_a_child_with_the_wrong_variant(self):
        wrong_root = self.make_category(self.app, "sticker root", None, self.effect_variant, self.active)
        wrong_child = self.make_category(self.app, "sticker child", wrong_root, self.effect_variant, self.active)
        serializer = FrameSerializer(
            data={
                "title": "Invalid frame",
                "category": str(wrong_child.pk),
                "frame_type": "frame",
                "editor": "frames",
                "ratio_width": "1.00",
                "ratio_height": "1.00",
                "status": "active",
                "image_picker": True,
                "sort_order": 1,
            }
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("category", serializer.errors)

    @override_settings(PUBLIC_API_KEY="test-key")
    def test_sticker_slide_and_font_lists_scope_app_and_active_status(self):
        variants = {
            code: AssetVariant.objects.create(code=code, label=code.title(), sort_order=index, is_active=True)
            for index, code in enumerate(("sticker", "slide", "font"), start=3)
        }
        slide_type = SlideType.objects.create(code="pro", label="Pro", sort_order=1, is_active=True)
        expected = {}
        other_app_categories = {}

        for code, model, values, public_path in (
            ("sticker", Sticker, {"image": "sticker.png"}, "/api/stickers/"),
            ("slide", Slide, {"slide_type": slide_type, "cover": "slide.png"}, "/api/slides/"),
            ("font", Font, {"file": "font.ttf"}, "/api/fonts/"),
        ):
            root = self.make_category(self.app, f"{code} root", None, variants[code], self.active)
            own_category = self.make_category(self.app, f"{code} child", root, variants[code], self.active)
            other_root = self.make_category(self.other_app, f"other {code} root", None, variants[code], self.active)
            other_category = self.make_category(self.other_app, f"other {code} child", other_root, variants[code], self.active)
            own = model.objects.create(
                title=f"own {code}", category=own_category, status=self.active, sort_order=1, **values
            )
            model.objects.create(
                title=f"other {code}", category=other_category, status=self.active, sort_order=2, **values
            )
            model.objects.create(
                title=f"inactive {code}", category=own_category, status=self.inactive, sort_order=3, **values
            )
            expected[public_path] = own.title

        for path, expected_title in expected.items():
            with self.subTest(path=path):
                response = self.client.get(
                    path,
                    HTTP_X_API_KEY="test-key",
                    HTTP_X_APP_NAME="app_a",
                )
                payload = json.loads(response.content)
                self.assertEqual(response.status_code, 200)
                self.assertEqual([row["title"] for row in payload["data"]], [expected_title])
