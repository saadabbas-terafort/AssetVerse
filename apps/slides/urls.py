from django.urls import path

from .views import SlideAdminViewSet, SlideDetailView, SlideView


urlpatterns = [
    path("api/slides/", SlideView.as_view(), name="slides-list"),
    path("api/slides/<uuid:pk>/", SlideDetailView.as_view(), name="slides-detail"),
    path("api/slides/admin/", SlideAdminViewSet.as_view({"get": "list", "post": "create"}), name="slides-admin-list"),
    path(
        "api/slides/admin/<uuid:pk>/",
        SlideAdminViewSet.as_view({"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}),
        name="slides-admin-detail",
    ),
]