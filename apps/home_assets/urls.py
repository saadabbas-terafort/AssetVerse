from django.urls import path

from .views import FrameView


urlpatterns = [
    path("api/frame", FrameView.as_view(), name="frame"),
]