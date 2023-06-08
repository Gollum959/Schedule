from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import (PtsRequestViewSet,
                       PlaceViewSet,
                       PtsConfigViewSet,
                       CityViewSet,
                       CameraTypeViewSet,
                       CameraBrendViewSet,
                       CameraModelViewSet,
                       OpticTypeViewSet,
                       OpticBrendViewSet,
                       OpticModelViewSet,
                       ServerTypelViewSet,
                       ServerPlayerTypeViewSet,
                       ServerBrendViewSet,
                       ServerModelViewSet,
                       MicrophoneTypelViewSet,
                       MicrophoneBrendlViewSet,
                       MicrophoneModelViewSet)

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('pts_requests', PtsRequestViewSet, basename='pts_requests')
router_v1.register('place', PlaceViewSet, basename='place')
router_v1.register('city', CityViewSet, basename='city')
router_v1.register('cameras/type', CameraTypeViewSet, basename='cameras_type')
router_v1.register(
    'cameras/brend',
    CameraBrendViewSet,
    basename='cameras_brend'
)
router_v1.register(
    'cameras/model',
    CameraModelViewSet,
    basename='cameras_model'
)
router_v1.register('optics/type', OpticTypeViewSet, basename='cameras_type')
router_v1.register('optics/brend', OpticBrendViewSet, basename='cameras_brend')
router_v1.register('optics/model', OpticModelViewSet, basename='cameras_model')
router_v1.register('servers/type', ServerTypelViewSet, basename='servers_type')
router_v1.register(
    'servers/player-type',
    ServerPlayerTypeViewSet,
    basename='servers_player_type'
)
router_v1.register(
    'servers/brend',
    ServerBrendViewSet,
    basename='servers_brend'
)
router_v1.register(
    'servers/model',
    ServerModelViewSet,
    basename='servers_model'
)
router_v1.register(
    'microphones/type',
    MicrophoneTypelViewSet,
    basename='microphones_type'
)
router_v1.register(
    'microphones/brend',
    MicrophoneBrendlViewSet,
    basename='microphones_brend'
)
router_v1.register(
    'microphones/model',
    MicrophoneModelViewSet,
    basename='microphones_model'
)
router_v1.register('pts_config', PtsConfigViewSet, basename='pts_config')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
