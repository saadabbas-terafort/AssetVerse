from django.urls import path

from .views import CategoryAdminViewSet, CategoryDetailView, CategoryView


urlpatterns = [
    path("api/categories/", CategoryView.as_view(), name="category-list"),
    path("api/categories/<uuid:pk>/", CategoryDetailView.as_view(), name="category-detail"),
    path(
        "api/categories/admin/",
        CategoryAdminViewSet.as_view({"get": "list", "post": "create"}),
        name="category-admin-list",
    ),
    path(
        "api/categories/admin/<uuid:pk>/",
        CategoryAdminViewSet.as_view({"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}),
        name="category-admin-detail",
    ),
]