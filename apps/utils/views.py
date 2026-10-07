from django.conf import settings
from django.core.exceptions import PermissionDenied
from rest_framework.generics import ListAPIView

from apps.app_settings.models import AppSetting
from apps.utils.permissions import PublicReadOnlyPermission
from apps.utils.responses import error_response, success_response


def get_active_app_from_request(request):
    app_name = request.headers.get("X-App-Name") or request.META.get("HTTP_X_APP_NAME")
    if not app_name:
        raise PermissionDenied("Missing X-App-Name header.")

    app = AppSetting.objects.filter(slug=app_name, is_active=True).first()
    if not app:
        raise PermissionDenied("Unknown or inactive app name.")

    public_key = request.headers.get("X-Api-Key") or request.META.get("HTTP_X_API_KEY")
    expected_key = getattr(settings, "PUBLIC_API_KEY", "")
    if not expected_key:
        raise PermissionDenied("Public API key is not configured.")
    if public_key != expected_key:
        raise PermissionDenied("Invalid X-Api-Key.")

    return app


class PublicListAPIView(ListAPIView):
    permission_classes = (PublicReadOnlyPermission,)

    def list(self, request, *args, **kwargs):
        try:
            get_active_app_from_request(request)
        except PermissionDenied as exc:
            return error_response(str(exc), status_code=403)

        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return success_response(serializer.data)