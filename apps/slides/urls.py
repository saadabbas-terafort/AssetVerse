from django.urls import path

from .views import SlideView


urlpatterns = [
    path("api/slide", SlideView.as_view(), name="slide"),
]