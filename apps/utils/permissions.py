from django.conf import settings
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import SAFE_METHODS, BasePermission, IsAdminUser


class PublicReadOnlyPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method not in SAFE_METHODS:
            return False

        public_key = request.headers.get("X-Api-Key") or request.META.get("HTTP_X_API_KEY")
        expected_key = getattr(settings, "PUBLIC_API_KEY", "")
        if not expected_key:
            raise PermissionDenied("Public API key is not configured.")
        if public_key != expected_key:
            raise PermissionDenied("Missing or invalid X-Api-Key header.")
        return True


class StaffPermission(IsAdminUser):
    """Restrict JSON write endpoints to authenticated staff accounts."""


class PublicAPIKeyPermission(BasePermission):
    def has_permission(self, request, view):
        public_key = request.headers.get("X-Api-Key") or request.META.get("HTTP_X_API_KEY")
        expected_key = getattr(settings, "PUBLIC_API_KEY", "")
        if not expected_key:
            raise PermissionDenied("Public API key is not configured.")
        if public_key != expected_key:
            raise PermissionDenied("Missing or invalid X-Api-Key header.")
        return True