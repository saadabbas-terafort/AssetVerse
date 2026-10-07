from django.core.exceptions import PermissionDenied
from rest_framework.views import APIView

from apps.utils.responses import error_response, success_response
from apps.utils.views import get_active_app_from_request
from apps.utils.viewsets import AppScopedAssetAdminViewSet

from .models import Frame, FrameAsset
from .serializers import FrameAssetSerializer, FrameSerializer


class FrameView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, *args, **kwargs):
        try:
            app = get_active_app_from_request(request)
        except PermissionDenied as exc:
            return error_response(str(exc), status_code=403)

        queryset = Frame.objects.select_related("category", "frame_type", "status").filter(
            category__app=app,
            status__code="active",
        )

        category_id = request.query_params.get("category")
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        serializer = FrameSerializer(queryset.order_by("sort_order", "title"), many=True, context={"request": request})
        return success_response(serializer.data)


class FrameDetailView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, pk, *args, **kwargs):
        try:
            app = get_active_app_from_request(request)
        except PermissionDenied as exc:
            return error_response(str(exc), status_code=403)

        frame = Frame.objects.select_related("category", "frame_type", "status").filter(
            category__app=app,
            pk=pk,
            status__code="active",
        ).first()

        if not frame:
            return error_response("Frame not found.", status_code=404)

        serializer = FrameSerializer(frame, context={"request": request})
        return success_response(serializer.data)


class FrameAdminViewSet(AppScopedAssetAdminViewSet):
    queryset = Frame.objects.select_related("category", "frame_type", "status").prefetch_related(
        "tags", "constraints", "assets__key", "assets__status"
    )
    serializer_class = FrameSerializer

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        frame_type = self.request.query_params.get("frame_type")
        if frame_type:
            queryset = queryset.filter(frame_type__code=frame_type)
        return queryset


class FrameAssetAdminViewSet(AppScopedAssetAdminViewSet):
    queryset = FrameAsset.objects.select_related("frame", "frame__category", "key", "status")
    serializer_class = FrameAssetSerializer
    category_filter = "frame__category_id"
    app_filter = "frame__category__app__slug"

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        frame_id = self.request.query_params.get("frame")
        if frame_id:
            queryset = queryset.filter(frame_id=frame_id)
        return queryset