from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import (PtsRequestViewSet,
                       PlaceViewSet,
                       PtsConfigViewSet,
                       CityViewSet,
                       CameraTypeViewSet,
                       CameraBrendViewSet,
                       CameraModelViewSet)

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('pts_requests', PtsRequestViewSet, basename='pts_requests')
router_v1.register('place', PlaceViewSet, basename='place')
router_v1.register('city', CityViewSet, basename='city')
router_v1.register('cameras/type', CameraTypeViewSet, basename='cameras_type')
router_v1.register('cameras/brend', CameraBrendViewSet, basename='cameras_brend')
router_v1.register('cameras/model', CameraModelViewSet, basename='cameras_model')
router_v1.register('pts_config', PtsConfigViewSet, basename='pts_config')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
