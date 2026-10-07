from django.urls import path

from .views import FontAdminViewSet, FontDetailView, FontView


urlpatterns = [
    path("api/fonts/", FontView.as_view(), name="fonts-list"),
    path("api/fonts/<uuid:pk>/", FontDetailView.as_view(), name="fonts-detail"),
    path("api/fonts/admin/", FontAdminViewSet.as_view({"get": "list", "post": "create"}), name="fonts-admin-list"),
    path(
        "api/fonts/admin/<uuid:pk>/",
        FontAdminViewSet.as_view({"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}),
        name="fonts-admin-detail",
    ),
]