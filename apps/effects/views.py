from apps.utils.views import PublicListAPIView

from .models import Effect
from .serializers import EffectSerializer


class EffectView(PublicListAPIView):
    queryset = Effect.objects.all()
    serializer_class = EffectSerializer