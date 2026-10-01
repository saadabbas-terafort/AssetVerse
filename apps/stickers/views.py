from apps.utils.views import PublicListAPIView

from .models import Sticker
from .serializers import StickerSerializer


class StickersView(PublicListAPIView):
    queryset = Sticker.objects.all()
    serializer_class = StickerSerializer