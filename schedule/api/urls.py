from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import PtsRequestViewSet

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('pts_requests', PtsRequestViewSet, basename='pts_requests')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
