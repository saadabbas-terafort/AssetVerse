from django.core.exceptions import PermissionDenied
from rest_framework.views import APIView

from apps.utils.responses import error_response, success_response
from apps.utils.views import get_active_app_from_request
from apps.utils.viewsets import EnvelopeModelViewSet

from .models import Category
from .serializers import CategorySerializer


class CategoryView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, *args, **kwargs):
        try:
            app = get_active_app_from_request(request)
        except PermissionDenied as exc:
            return error_response(str(exc), status_code=403)

        queryset = Category.objects.select_related(
            "app", "orientation", "tag", "section", "status", "variant", "parent"
        ).filter(app=app, status__code="active")
        section = request.query_params.get("section")
        variant = request.query_params.get("variant")
        parent_id = request.query_params.get("parent_id")
        parent_flag = request.query_params.get("parent")

        if section:
            queryset = queryset.filter(section__code=section)
        if variant:
            queryset = queryset.filter(variant__code=variant)
        if parent_id:
            queryset = queryset.filter(parent_id=parent_id)
        elif parent_flag is not None and parent_flag.lower() in {"true", "false"}:
            queryset = queryset.filter(parent__isnull=parent_flag.lower() == "true")

        serializer = CategorySerializer(queryset.order_by("sort_order", "title"), many=True, context={"request": request})
        return success_response(serializer.data)


class CategoryDetailView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, pk, *args, **kwargs):
        try:
            app = get_active_app_from_request(request)
        except PermissionDenied as exc:
            return error_response(str(exc), status_code=403)

        category = Category.objects.select_related(
            "app", "orientation", "tag", "section", "status", "variant", "parent"
        ).filter(app=app, pk=pk, status__code="active").first()

        if not category:
            return error_response("Category not found.", status_code=404)

        serializer = CategorySerializer(category, context={"request": request})
        return success_response(serializer.data)


class CategoryAdminViewSet(EnvelopeModelViewSet):
    queryset = Category.objects.select_related(
        "app", "orientation", "tag", "section", "status", "variant", "parent"
    )
    serializer_class = CategorySerializer

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        app_slug = self.request.query_params.get("app") or self.request.query_params.get("app_name")
        variant = self.request.query_params.get("variant")
        if app_slug:
            queryset = queryset.filter(app__slug=app_slug)
        if variant:
            queryset = queryset.filter(variant__code=variant)
        return queryset