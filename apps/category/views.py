from apps.utils.views import PublicListAPIView

from .models import Category
from .serializers import CategorySerializer


class CategoryView(PublicListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer