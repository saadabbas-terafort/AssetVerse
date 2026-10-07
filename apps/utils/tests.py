from django.test import SimpleTestCase
from rest_framework import serializers
from rest_framework.relations import ManyRelatedField, PrimaryKeyRelatedField

from apps.category.serializers import CategorySerializer
from apps.effects.serializers import EffectSerializer
from apps.fonts.serializers import FontSerializer
from apps.home_assets.serializers import FrameAssetSerializer, FrameConstraintSerializer, FrameSerializer
from apps.slides.serializers import SlideSerializer
from apps.stickers.serializers import StickerSerializer
from apps.utils.serializer_fields import ActiveCodeRelatedField, AppSlugField


class AssetRelatedFieldSerializerTests(SimpleTestCase):
    def test_category_uses_nested_app_and_writable_lookup_codes(self):
        fields = CategorySerializer().fields

        self.assertIsInstance(fields["app"], AppSlugField)
        self.assertIsInstance(fields["parent"], PrimaryKeyRelatedField)
        for field_name in ("orientation", "tag", "section", "status", "variant"):
            with self.subTest(field=field_name):
                self.assertIsInstance(fields[field_name], ActiveCodeRelatedField)
                self.assertFalse(fields[field_name].read_only)

    def test_asset_serializers_accept_category_ids_and_lookup_codes(self):
        serializer_fields = (
            (EffectSerializer, ("effect_type", "status"), ("tags",)),
            (FontSerializer, ("status",), ("tags",)),
            (FrameSerializer, ("frame_type", "status"), ("tags",)),
            (FrameAssetSerializer, ("key", "status"), ()),
            (SlideSerializer, ("slide_type", "status"), ()),
            (StickerSerializer, ("status",), ("tags",)),
        )

        for serializer_class, code_fields, many_fields in serializer_fields:
            fields = serializer_class().fields
            with self.subTest(serializer=serializer_class.__name__):
                if "category" in fields:
                    self.assertIsInstance(fields["category"], PrimaryKeyRelatedField)
                if "frame" in fields:
                    self.assertIsInstance(fields["frame"], PrimaryKeyRelatedField)
                for field_name in code_fields:
                    with self.subTest(field=field_name):
                        self.assertIsInstance(fields[field_name], ActiveCodeRelatedField)
                        self.assertFalse(fields[field_name].read_only)
                for field_name in many_fields:
                    with self.subTest(field=field_name):
                        self.assertIsInstance(fields[field_name], ManyRelatedField)
                        self.assertIsInstance(fields[field_name].child_relation, ActiveCodeRelatedField)

    def test_frame_read_contract_nests_constraints_and_layers(self):
        fields = FrameSerializer().fields

        self.assertIsInstance(fields["constraints"], serializers.ListSerializer)
        self.assertIsInstance(fields["constraints"].child, FrameConstraintSerializer)
        self.assertIsInstance(fields["assets"], serializers.ListSerializer)
