from django.urls import path

from .views import CategoryView


urlpatterns = [
    path("api/category", CategoryView.as_view(), name="category"),
]