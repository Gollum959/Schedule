from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ReadOnlyModelViewSet
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from api.custom_filters import CustomDjangoFilterBackend
from api.serializers import (PtsRequestSerializer, PlaceSerializer,
                             PtsConfigSerializer, CitySerializer,
                             CameraBrendMatrixSerializer,
                             CameraTypeSerializer,
                             CameraModelSerializer)
from pts_requests.models import PtsRequest
from place_broadcast.models import PlaceConstructor, PlaceCity
from pts_config.models import PtsConstructor, Camera, CameraModelBrend


# Cameras API viewsets

class CameraTypeViewSet(ReadOnlyModelViewSet):
    serializer_class = CameraTypeSerializer
    queryset = Camera.objects.all()


class CameraBrendViewSet(ReadOnlyModelViewSet):
    serializer_class = CameraBrendMatrixSerializer
    queryset = Camera.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name',)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'type_pts',
                openapi.IN_QUERY,
                description='Параметр типа ПТС, 1-Александрина, 2-Новые ПТС',
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                name='name',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description=('Параметр фильтра по типу камеры '
                             '(Обычная, Радиокамера, PTZ, Миникамера,'
                             ' SSM Камера)'),
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class CameraModelViewSet(ReadOnlyModelViewSet):
    serializer_class = CameraModelSerializer
    queryset = CameraModelBrend.objects.all()

    filter_backends = (CustomDjangoFilterBackend,)
    filterset_fields = ('brend__type_pts', 'type__name')

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     type_param = self.request.query_params.get('brend__type_pts')

    #     if type_param:
    #         # queryset = queryset.filter(Q(brend__type_pts=type_param) | Q(brend__type_pts__isnull=True))
    #         print(queryset)
    #     return queryset


# Places API viewsets

class CityViewSet(ReadOnlyModelViewSet):
    serializer_class = CitySerializer
    queryset = PlaceCity.objects.all()


class PlaceViewSet(ReadOnlyModelViewSet):
    serializer_class = PlaceSerializer
    queryset = PlaceConstructor.objects.all()


# Configs API viewsets

class PtsConfigViewSet(ReadOnlyModelViewSet):
    serializer_class = PtsConfigSerializer
    queryset = PtsConstructor.objects.all()


# PTS_requests API viewsets

class PtsRequestViewSet(ReadOnlyModelViewSet):
    serializer_class = PtsRequestSerializer
    queryset = PtsRequest.objects.all()
