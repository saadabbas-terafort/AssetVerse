from apps.utils.views import PublicListAPIView

from .models import Slide
from .serializers import SlideSerializer


class SlideView(PublicListAPIView):
    queryset = Slide.objects.all()
    serializer_class = SlideSerializer