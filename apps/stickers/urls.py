from django.urls import path

from .views import StickerAdminViewSet, StickerDetailView, StickersView


urlpatterns = [
    path("api/stickers/", StickersView.as_view(), name="stickers-list"),
    path("api/stickers/<uuid:pk>/", StickerDetailView.as_view(), name="stickers-detail"),
    path("api/stickers/admin/", StickerAdminViewSet.as_view({"get": "list", "post": "create"}), name="stickers-admin-list"),
    path(
        "api/stickers/admin/<uuid:pk>/",
        StickerAdminViewSet.as_view({"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}),
        name="stickers-admin-detail",
    ),
]