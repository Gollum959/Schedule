from rest_framework.viewsets import ReadOnlyModelViewSet

from api.serializers import PtsRequestSerializer
from pts_requests.models import PtsRequest


class PtsRequestViewSet(ReadOnlyModelViewSet):
    serializer_class = PtsRequestSerializer
    queryset = PtsRequest.objects.all()
