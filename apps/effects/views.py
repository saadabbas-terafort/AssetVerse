from django.core.exceptions import PermissionDenied
from rest_framework.views import APIView

from apps.utils.responses import error_response, success_response
from apps.utils.views import get_active_app_from_request
from apps.utils.viewsets import AppScopedAssetAdminViewSet

from .models import Effect
from .serializers import EffectSerializer


class EffectView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, *args, **kwargs):
        try:
            app = get_active_app_from_request(request)
        except PermissionDenied as exc:
            return error_response(str(exc), status_code=403)

        queryset = Effect.objects.select_related("category", "effect_type", "status").filter(
            category__app=app,
            status__code="active",
        )
        category_id = request.query_params.get("category")
        effect_type = request.query_params.get("effect_type")
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if effect_type:
            queryset = queryset.filter(effect_type__code=effect_type)

        serializer = EffectSerializer(queryset.order_by("sort_order", "title"), many=True, context={"request": request})
        return success_response(serializer.data)


class EffectDetailView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, pk, *args, **kwargs):
        try:
            app = get_active_app_from_request(request)
        except PermissionDenied as exc:
            return error_response(str(exc), status_code=403)

        effect = Effect.objects.select_related("category", "effect_type", "status").filter(
            category__app=app,
            pk=pk,
            status__code="active",
        ).first()
        if not effect:
            return error_response("Effect not found.", status_code=404)

        serializer = EffectSerializer(effect, context={"request": request})
        return success_response(serializer.data)


class EffectAdminViewSet(AppScopedAssetAdminViewSet):
    queryset = Effect.objects.select_related("category", "effect_type", "status").prefetch_related("tags")
    serializer_class = EffectSerializer

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        effect_type = self.request.query_params.get("effect_type")
        if effect_type:
            queryset = queryset.filter(effect_type__code=effect_type)
        return queryset