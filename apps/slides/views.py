from django.core.exceptions import PermissionDenied
from rest_framework.views import APIView

from apps.utils.responses import error_response, success_response
from apps.utils.views import get_active_app_from_request
from apps.utils.viewsets import AppScopedAssetAdminViewSet

from .models import Slide
from .serializers import SlideSerializer


class SlideView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, *args, **kwargs):
        try:
            app = get_active_app_from_request(request)
        except PermissionDenied as exc:
            return error_response(str(exc), status_code=403)

        queryset = Slide.objects.select_related("category", "slide_type", "status").filter(category__app=app, status__code="active")
        category_id = request.query_params.get("category")
        slide_type = request.query_params.get("slide_type")
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if slide_type:
            queryset = queryset.filter(slide_type__code=slide_type)

        serializer = SlideSerializer(queryset.order_by("sort_order", "title"), many=True, context={"request": request})
        return success_response(serializer.data)


class SlideDetailView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, pk, *args, **kwargs):
        try:
            app = get_active_app_from_request(request)
        except PermissionDenied as exc:
            return error_response(str(exc), status_code=403)

        slide = Slide.objects.select_related("category", "slide_type", "status").filter(
            category__app=app,
            pk=pk,
            status__code="active",
        ).first()
        if not slide:
            return error_response("Slide not found.", status_code=404)

        serializer = SlideSerializer(slide, context={"request": request})
        return success_response(serializer.data)


class SlideAdminViewSet(AppScopedAssetAdminViewSet):
    queryset = Slide.objects.select_related("category", "slide_type", "status")
    serializer_class = SlideSerializer

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        slide_type = self.request.query_params.get("slide_type")
        if slide_type:
            queryset = queryset.filter(slide_type__code=slide_type)
        return queryset