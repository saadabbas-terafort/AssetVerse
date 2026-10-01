from django.urls import path

from .views import StickersView


urlpatterns = [
    path("api/sticker", StickersView.as_view(), name="sticker"),
]