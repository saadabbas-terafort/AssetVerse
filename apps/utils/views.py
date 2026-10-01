from rest_framework.generics import ListAPIView

from apps.utils.permissions import PublicReadOnlyPermission
from apps.utils.responses import success_response


class PublicListAPIView(ListAPIView):
    permission_classes = (PublicReadOnlyPermission,)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return success_response(serializer.data)