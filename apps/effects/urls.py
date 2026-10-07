from django.urls import path

from .views import EffectAdminViewSet, EffectDetailView, EffectView


urlpatterns = [
    path("api/effects/", EffectView.as_view(), name="effects-list"),
    path("api/effects/<uuid:pk>/", EffectDetailView.as_view(), name="effects-detail"),
    path("api/effects/admin/", EffectAdminViewSet.as_view({"get": "list", "post": "create"}), name="effects-admin-list"),
    path(
        "api/effects/admin/<uuid:pk>/",
        EffectAdminViewSet.as_view({"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}),
        name="effects-admin-detail",
    ),
]