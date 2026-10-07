from django.core.exceptions import PermissionDenied
from rest_framework.views import APIView

from apps.utils.responses import error_response, success_response
from apps.utils.views import get_active_app_from_request
from apps.utils.viewsets import AppScopedAssetAdminViewSet

from .models import Sticker
from .serializers import StickerSerializer


class StickersView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, *args, **kwargs):
        try:
            app = get_active_app_from_request(request)
        except PermissionDenied as exc:
            return error_response(str(exc), status_code=403)

        queryset = Sticker.objects.select_related("category", "status").filter(category__app=app, status__code="active")
        category_id = request.query_params.get("category")
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        serializer = StickerSerializer(queryset.order_by("sort_order", "title"), many=True, context={"request": request})
        return success_response(serializer.data)


class StickerDetailView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, pk, *args, **kwargs):
        try:
            app = get_active_app_from_request(request)
        except PermissionDenied as exc:
            return error_response(str(exc), status_code=403)

        sticker = Sticker.objects.select_related("category", "status").filter(
            category__app=app,
            pk=pk,
            status__code="active",
        ).first()
        if not sticker:
            return error_response("Sticker not found.", status_code=404)

        serializer = StickerSerializer(sticker, context={"request": request})
        return success_response(serializer.data)


class StickerAdminViewSet(AppScopedAssetAdminViewSet):
    queryset = Sticker.objects.select_related("category", "status").prefetch_related("tags")
    serializer_class = StickerSerializer