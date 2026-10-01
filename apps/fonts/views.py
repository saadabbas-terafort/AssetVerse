from apps.utils.views import PublicListAPIView

from .models import Font
from .serializers import FontSerializer


class FontView(PublicListAPIView):
    queryset = Font.objects.all()
    serializer_class = FontSerializer