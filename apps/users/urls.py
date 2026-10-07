from django.urls import path

from .views import DeviceAuthView

urlpatterns = [
    path("api/users/auth/", DeviceAuthView.as_view(), name="device-auth"),
]
