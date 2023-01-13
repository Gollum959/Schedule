from django.urls import path
from place_broadcast.views import PlacesBroadcastView, PlacesBroadcastDetail

app_name = 'pts_broadcast'

urlpatterns = [
    path('', PlacesBroadcastView.as_view(), name='places'),
    path(
        '<int:pk>/',
        PlacesBroadcastDetail.as_view(),
        name='place_detail'
    ),
]
