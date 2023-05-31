from rest_framework.viewsets import ReadOnlyModelViewSet

from api.serializers import (PtsRequestSerializer, PlaceSerializer,
                             PtsConfigSerializer)
from pts_requests.models import PtsRequest
from place_broadcast.models import PlaceConstructor
from pts_config.models import PtsConstructor


class PlaceViewSet(ReadOnlyModelViewSet):
    serializer_class = PlaceSerializer
    queryset = PlaceConstructor.objects.all()


class PtsConfigViewSet(ReadOnlyModelViewSet):
    serializer_class = PtsConfigSerializer
    queryset = PtsConstructor.objects.all()


class PtsRequestViewSet(ReadOnlyModelViewSet):
    serializer_class = PtsRequestSerializer
    queryset = PtsRequest.objects.all()
