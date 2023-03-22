from django.urls import path

from pts_requests import views


app_name = 'pts_requests'

urlpatterns = [
    path('', views.PtsRequestsView.as_view(), name='index'),
    path(
        'request/<int:pk>/',
        views.PtsRequestDetail.as_view(),
        name='request_detail'
    ),
    path('create/', views.PtsRequestCreate.as_view(), name='request_create'),
    path('create/<int:pk>/', views.PtsRequestEdit.as_view(), name='request_edit'),
    path(
        'send_request/<int:pk>/',
        views.change_status_to_on_approval,
        name='request_change_status'
    ),
    path(
        'remove_draft/<int:pk>/',
        views.remove_draft_pts_request,
        name='draft_request_remove'
    ),
    path('ajax/load-places/', views.load_places, name='ajax_load_places'),
    path('ajax/load-cfg/', views.load_pts_cfg, name='ajax_load_cfg'),
    path(
        'ajax/load-event-types/',
        views.load_event_type,
        name='ajax_load_event_types'
    ),
    path(
        'ajax/load-request-cfg-cam/',
        views.load_cameras_in_request,
        name='ajax_load_cfg_cam'
    ),
    path(
        'ajax/load-request-cfg-optic/',
        views.load_optics_in_request,
        name='ajax_load_cfg_optic'
    ),
    path(
        'ajax/load-request-cfg-server/',
        views.load_servers_in_request,
        name='ajax_load_cfg_server'
    ),
    path(
        'ajax/load-request-cfg-gfx/',
        views.load_gfx_in_request,
        name='ajax_load_cfg_gfx'
    ),
    path(
        'ajax/load-request-cfg-micro/',
        views.load_micro_in_request,
        name='ajax_load_cfg_micro'
    ),
]

htmx_urlpatterns = [
    path(
        'request/<int:pk>/trakt-edit/',
        views.time_trakt_edit_form,
        name='trakt_time_edit'
    ),
    path(
        'request/<int:pk>/travel-edit/',
        views.time_travel_edit_form,
        name='travel_time_edit'
    ),
    path(
        'request/<int:pk>/config-choice-pts/',
        views.config_choice_pts_edit_form,
        name='config_choice_pts'
    ),
]

urlpatterns += htmx_urlpatterns
