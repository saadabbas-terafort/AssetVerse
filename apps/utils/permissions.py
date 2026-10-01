from rest_framework.permissions import SAFE_METHODS, BasePermission


class PublicReadOnlyPermission(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS