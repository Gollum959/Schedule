from django.urls import path
from place_broadcast.views import (CitiesBroadcastView,
                                   PlacesBroadcastView,
                                   PlacesBroadcastDetail,
                                   PlacesBroadcastCreate,
                                   PlacesBroadcastEdit,
                                   CityBroadcastCreate,
                                   place_delete)


app_name = 'pts_broadcast'

urlpatterns = [
    path('', CitiesBroadcastView.as_view(), name='places'),
    path(
        '<int:pk>/',
        PlacesBroadcastDetail.as_view(),
        name='place_detail'
    ),
    path(
        'city_create/',
        CityBroadcastCreate.as_view(),
        name='city_create'
    ),
    path(
        'create/',
        PlacesBroadcastCreate.as_view(),
        name='place_create'
    ),
    path(
        'create/<int:pk>/',
        PlacesBroadcastEdit.as_view(),
        name='place_edit'
    ),
    path(
        'ajax/load-places/',
        PlacesBroadcastView.as_view(),
        name='ajax_load_places'
    ),
    path(
        'delete/<int:pk>/',
        place_delete,
        name='place_delete'
    ),
]
