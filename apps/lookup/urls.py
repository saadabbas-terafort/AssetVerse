from django.urls import path

from .views import LookupBundleView, TagDetailView, TagListView

urlpatterns = [
    path("api/lookups/", LookupBundleView.as_view(), name="lookup-bundle"),
    path("api/lookups/tags/", TagListView.as_view(), name="lookup-tags"),
    path("api/lookups/tags/<uuid:pk>/", TagDetailView.as_view(), name="lookup-tag-detail"),
]
