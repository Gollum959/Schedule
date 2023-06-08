from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.viewsets import ReadOnlyModelViewSet
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from api.custom_filters import (CameraDjangoFilterBackend,
                                OpticDjangoFilterBackend,
                                MicrophoneBrendFilter)
from api.serializers import (PtsRequestSerializer, PlaceSerializer,
                             PtsConfigSerializer, CitySerializer,
                             CameraBrendMatrixSerializer,
                             CameraTypeSerializer,
                             CameraModelSerializer,
                             OpticTypeSerializer,
                             OpticBrendMatrixSerializer,
                             OpticModelSerializer,
                             ServerTypeSerializer,
                             ServerPlayerTypeSerializer,
                             ServerBrendSerializer,
                             ServerModelSerializer,
                             MicrophoneTypeSerializer,
                             MicrophoneBrendSerializer,
                             MicrophoneModelSerializer)
from pts_requests.models import PtsRequest
from place_broadcast.models import PlaceConstructor, PlaceCity
from pts_config.models import (PtsConstructor,
                               Camera,
                               CameraModelBrend,
                               Optic,
                               OpticModelBrend,
                               ServerRecordingRepeatType,
                               ServerPlayerType,
                               ServerRecordingRepeatBrend,
                               ServerRecordingRepeatModelBrend,
                               MicrophoneType,
                               MicrophoneBrend,
                               MicrophoneModelBrend)


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

    filter_backends = (CameraDjangoFilterBackend,)
    filterset_fields = ('brend__type_pts', 'type', 'brend')

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'brend__type_pts',
                openapi.IN_QUERY,
                description='Параметр типа ПТС, 1-Александрина, 2-Новые ПТС',
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                name='type',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description=('Параметр фильтра по типу камеры '),
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


# Optics API viewsets

class OpticTypeViewSet(ReadOnlyModelViewSet):

    serializer_class = OpticTypeSerializer
    queryset = Optic.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('visible_to_user',)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'visible_to_user',
                openapi.IN_QUERY,
                description=('Фильтр 1, 0 видна ли данная '
                             'оптика режиссеру или нет'),
                type=openapi.TYPE_INTEGER
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class OpticBrendViewSet(ReadOnlyModelViewSet):

    serializer_class = OpticBrendMatrixSerializer
    queryset = Optic.objects.all()
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
                description=('Параметр фильтра по типу оптики '
                             '(22х, 13х, 14х, 40х, 23х,	76х, 80х, 88х, 24х)'),
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class OpticModelViewSet(ReadOnlyModelViewSet):

    serializer_class = OpticModelSerializer
    queryset = OpticModelBrend.objects.all()
    filter_backends = (OpticDjangoFilterBackend,)
    filterset_fields = ('brend__type_pts', 'type__name')

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'brend__type_pts',
                openapi.IN_QUERY,
                description='Параметр типа ПТС, 1-Александрина, 2-Новые ПТС',
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                name='type__name',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description=('Параметр фильтра по типу оптики '
                             '(22х, 13х, 14х, 40х, 23х,	76х, 80х, 88х, 24х)'),
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


# Servers API viewsets

class ServerTypelViewSet(ReadOnlyModelViewSet):

    serializer_class = ServerTypeSerializer
    queryset = ServerRecordingRepeatType.objects.all()


class ServerPlayerTypeViewSet(ReadOnlyModelViewSet):

    serializer_class = ServerPlayerTypeSerializer
    queryset = ServerPlayerType.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('visible_to_user', 'rec_rep_type')

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'visible_to_user',
                openapi.IN_QUERY,
                description=('Фильтр 1, 0 видна ли данная '
                             'оптика режиссеру или нет'),
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'rec_rep_type',
                openapi.IN_QUERY,
                description=('1, 2 Сервер повтора, сервер записи '
                             'соответственно'),
                type=openapi.TYPE_INTEGER
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ServerBrendViewSet(ReadOnlyModelViewSet):

    serializer_class = ServerBrendSerializer
    queryset = ServerRecordingRepeatBrend.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('type_pts', )

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'type_pts',
                openapi.IN_QUERY,
                description='Параметр типа ПТС, 1-Александрина, 2-Новые ПТС',
                type=openapi.TYPE_INTEGER
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ServerModelViewSet(ReadOnlyModelViewSet):

    serializer_class = ServerModelSerializer
    queryset = ServerRecordingRepeatModelBrend.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('brend', 'brend__type_pts')

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'brend__type_pts',
                openapi.IN_QUERY,
                description='Параметр типа ПТС, 1-Александрина, 2-Новые ПТС',
                type=openapi.TYPE_INTEGER
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


# Microphones' block


class MicrophoneTypelViewSet(ReadOnlyModelViewSet):

    serializer_class = MicrophoneTypeSerializer
    queryset = MicrophoneType.objects.all()


class MicrophoneBrendlViewSet(ReadOnlyModelViewSet):

    serializer_class = MicrophoneBrendSerializer
    queryset = MicrophoneBrend.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['type_micro', 'type_pts']

    def get_queryset(self):
        queryset = super().get_queryset()
        type_micro = self.request.query_params.get('type_micro', None)
        type_pts = self.request.query_params.get('type_pts', None)
        if type_micro is not None:
            queryset = queryset.filter(microphonemodelbrend__type_micro=type_micro).distinct()
        if type_pts is not None:
            queryset = queryset.filter(microphonemodelbrend__type_pts=type_pts).distinct()
        return queryset

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'type_pts',
                openapi.IN_QUERY,
                description='Параметр типа ПТС, 1-Александрина, 2-Новые ПТС',
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'type_micro',
                openapi.IN_QUERY,
                description='Параметр типа микрофона',
                type=openapi.TYPE_INTEGER
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class MicrophoneModelViewSet(ReadOnlyModelViewSet):

    serializer_class = MicrophoneModelSerializer
    queryset = MicrophoneModelBrend.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('brend', 'type_micro', 'type_pts')


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
