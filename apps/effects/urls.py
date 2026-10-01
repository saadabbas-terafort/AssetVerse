from django.urls import path

from .views import EffectView


urlpatterns = [
    path("api/effect", EffectView.as_view(), name="effect"),
]