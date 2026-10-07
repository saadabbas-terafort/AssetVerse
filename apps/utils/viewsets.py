from rest_framework import status, viewsets
from rest_framework.response import Response

from apps.utils.permissions import StaffPermission


class EnvelopeModelViewSet(viewsets.ModelViewSet):
    permission_classes = (StaffPermission,)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({"status": 200, "data": serializer.data, "message": "Success"})

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response({"status": 200, "data": serializer.data, "message": "Success"})

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"status": 201, "data": serializer.data, "message": "Created successfully"},
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"status": 200, "data": serializer.data, "message": "Updated successfully"})

    def destroy(self, request, *args, **kwargs):
        self.perform_destroy(self.get_object())
        return Response({"status": 200, "data": {}, "message": "Deleted successfully"})


class AppScopedAssetAdminViewSet(EnvelopeModelViewSet):
    category_filter = "category_id"
    app_filter = "category__app__slug"

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        category_id = self.request.query_params.get("category")
        app_slug = self.request.query_params.get("app") or self.request.query_params.get("app_name")
        if category_id:
            queryset = queryset.filter(**{self.category_filter: category_id})
        if app_slug:
            queryset = queryset.filter(**{self.app_filter: app_slug})
        return queryset