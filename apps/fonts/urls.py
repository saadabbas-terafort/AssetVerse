from django.urls import path

from .views import FontView


urlpatterns = [
    path("api/font", FontView.as_view(), name="font"),
]