from django.urls import path

from .views import FrameAdminViewSet, FrameAssetAdminViewSet, FrameDetailView, FrameView


urlpatterns = [
    path("api/home-assets/frames/", FrameView.as_view(), name="frame-list"),
    path("api/home-assets/frames/<uuid:pk>/", FrameDetailView.as_view(), name="frame-detail"),
    path(
        "api/home-assets/admin/frames/",
        FrameAdminViewSet.as_view({"get": "list", "post": "create"}),
        name="frame-admin-list",
    ),
    path(
        "api/home-assets/admin/frames/<uuid:pk>/",
        FrameAdminViewSet.as_view({"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}),
        name="frame-admin-detail",
    ),
    path(
        "api/home-assets/admin/frame-assets/",
        FrameAssetAdminViewSet.as_view({"get": "list", "post": "create"}),
        name="frame-asset-admin-list",
    ),
    path(
        "api/home-assets/admin/frame-assets/<uuid:pk>/",
        FrameAssetAdminViewSet.as_view({"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}),
        name="frame-asset-admin-detail",
    ),
]