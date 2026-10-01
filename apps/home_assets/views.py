from apps.utils.views import PublicListAPIView

from .models import Frame
from .serializers import FrameSerializer


class FrameView(PublicListAPIView):
    queryset = Frame.objects.all()
    serializer_class = FrameSerializer