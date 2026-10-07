from django.core.exceptions import PermissionDenied
from rest_framework.views import APIView

from apps.utils.responses import error_response, success_response
from apps.utils.views import get_active_app_from_request
from apps.utils.viewsets import AppScopedAssetAdminViewSet

from .models import Font
from .serializers import FontSerializer


class FontView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, *args, **kwargs):
        try:
            app = get_active_app_from_request(request)
        except PermissionDenied as exc:
            return error_response(str(exc), status_code=403)

        queryset = Font.objects.select_related("category", "status").filter(category__app=app, status__code="active")
        category_id = request.query_params.get("category")
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        serializer = FontSerializer(queryset.order_by("sort_order", "title"), many=True, context={"request": request})
        return success_response(serializer.data)


class FontDetailView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, pk, *args, **kwargs):
        try:
            app = get_active_app_from_request(request)
        except PermissionDenied as exc:
            return error_response(str(exc), status_code=403)

        font = Font.objects.select_related("category", "status").filter(
            category__app=app,
            pk=pk,
            status__code="active",
        ).first()
        if not font:
            return error_response("Font not found.", status_code=404)

        serializer = FontSerializer(font, context={"request": request})
        return success_response(serializer.data)


class FontAdminViewSet(AppScopedAssetAdminViewSet):
    queryset = Font.objects.select_related("category", "status").prefetch_related("tags")
    serializer_class = FontSerializer