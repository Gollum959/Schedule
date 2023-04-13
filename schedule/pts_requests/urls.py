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
    path(
        'create/<int:pk>/',
        views.PtsRequestEdit.as_view(),
        name='request_edit'
    ),
    path(
        'remove_draft/<int:pk>/',
        views.remove_draft_pts_request,
        name='draft_request_remove'
    ),
]

status_request_change_urlpatterns = [
    path(
        'request/on-approval/<int:pk>/',
        views.change_status_to_on_approval,
        name='request_change_status'
    ),
    path(
        'request/cancel/<int:pk>/',
        views.change_status_to_cancel,
        name='request_change_status_cancel'
    ),
    path(
        'request/reject/<int:pk>/',
        views.change_status_to_reject,
        name='request_change_status_reject'
    ),
    path(
        'request/soundman/<int:pk>/',
        views.change_status_to_on_soundman,
        name='request_change_status_soundman'
    ),
    path(
        'request/after-soundman/<int:pk>/',
        views.change_status_to_final,
        name='request_change_status_after_soundman'
    ),
    path(
        'request/approved/<int:pk>/',
        views.change_status_to_dptr,
        name='request_change_status_dptr'
    ),
]

urlpatterns += status_request_change_urlpatterns

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
    path(
        'request/<int:pk>/config-cameras/',
        views.config_cameras_edit_form,
        name='config_cameras_edit'
    ),
    path(
        'request/<int:pk>/config-optics/',
        views.config_optics_edit_form,
        name='config_optics_edit'
    ),
    path(
        'request/<int:pk>/config-servers/',
        views.config_servers_edit_form,
        name='config_servers_edit'
    ),
    path(
        'request/<int:pk>/config-microphones/',
        views.config_microphones_edit_form,
        name='config_microphones_edit'
    ),
]

urlpatterns += htmx_urlpatterns

ajax_dropdown_urlpatterns = [
    path('ajax/load-places/', views.load_places, name='ajax_load_places'),
    path('ajax/load-cfg/', views.load_pts_cfg, name='ajax_load_cfg'),
    path(
        'ajax/load-event-types/',
        views.load_event_type,
        name='ajax_load_event_types'
    ),
    path(
        'ajax/load-cfg-detail/',
        views.load_cfg_detail,
        name='ajax_load_cfg_detail'
    ),
]

urlpatterns += ajax_dropdown_urlpatterns
