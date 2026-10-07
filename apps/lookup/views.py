from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

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
from apps.utils.permissions import PublicAPIKeyPermission
from apps.utils.responses import absolute_file_url, error_response, success_response


class LookupBundleView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        tags = Tag.objects.filter(is_active=True).order_by("sort_order", "label")
        lookup_models = {
            "orientations": Orientation,
            "statuses": RecordStatus,
            "variants": AssetVariant,
            "frame_keys": FrameKey,
            "frame_types": FrameType,
            "effect_types": EffectType,
            "slide_types": SlideType,
        }
        bundle = {
            key: [
                {"code": item.code, "label": item.label}
                for item in model.objects.filter(is_active=True).order_by("sort_order", "label")
            ]
            for key, model in lookup_models.items()
        }
        tag_groups = {
            "tags": Tag.TagType.AVAILABILITY,
            "sections": Tag.TagType.LISTING,
            "screen_tags": Tag.TagType.SCREEN,
            "variant_tags": Tag.TagType.VARIANT,
            "hashtags": Tag.TagType.HASHTAG,
            "locales": Tag.TagType.LOCALE,
        }
        for key, tag_type in tag_groups.items():
            bundle[key] = [
                {
                    "code": item.code,
                    "label": item.label,
                    "tag_type": item.tag_type,
                    "icon": absolute_file_url(request, item.icon),
                }
                for item in tags.filter(tag_type=tag_type)
            ]
        return success_response(bundle)


class TagListView(APIView):
    authentication_classes = []
    permission_classes = (PublicAPIKeyPermission,)

    def get(self, request, *args, **kwargs):
        tag_type = request.query_params.get("type")
        queryset = Tag.objects.filter(is_active=True)
        if tag_type:
            queryset = queryset.filter(tag_type=tag_type)

        payload = [
            {"code": item.code, "label": item.label, "tag_type": item.tag_type, "icon": absolute_file_url(request, item.icon)}
            for item in queryset.order_by("sort_order", "label")
        ]
        return success_response(payload)


class TagDetailView(APIView):
    authentication_classes = []
    permission_classes = (PublicAPIKeyPermission,)

    def get(self, request, pk, *args, **kwargs):
        tag = Tag.objects.filter(pk=pk, is_active=True).first()
        if not tag:
            return error_response("Tag not found.", status_code=404)

        payload = {
            "id": str(tag.id),
            "code": tag.code,
            "label": tag.label,
            "tag_type": tag.tag_type,
            "icon": absolute_file_url(request, tag.icon),
        }
        return success_response(payload)
