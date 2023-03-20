from django.urls import path
from pts_requests.views import (
    PtsRequestsView, PtsRequestDetail, PtsRequestCreate,
    PtsRequestEdit, PtsRequestModerate, load_places, load_pts_cfg,
    load_event_type, change_status_to_on_approval, remove_draft_pts_request,
    load_cameras_in_request, load_optics_in_request, load_servers_in_request,
    load_gfx_in_request, load_micro_in_request, printbtk,
)

app_name = 'pts_requests'

urlpatterns = [
    path('', PtsRequestsView.as_view(), name='index'),
    path(
        'request/<int:pk>/',
        PtsRequestDetail.as_view(),
        name='request_detail'
    ),
    path('create/', PtsRequestCreate.as_view(), name='request_create'),
    path('create/<int:pk>/', PtsRequestEdit.as_view(), name='request_edit'),
    path(
        'moderate/<int:pk>/',
        PtsRequestModerate.as_view(),
        name='request_moderate'
    ),
    path(
        'send_request/<int:pk>/',
        change_status_to_on_approval,
        name='request_change_status'
    ),
    path(
        'remove_draft/<int:pk>/',
        remove_draft_pts_request,
        name='draft_request_remove'
    ),
    path('ajax/load-places/', load_places, name='ajax_load_places'),
    path('ajax/load-cfg/', load_pts_cfg, name='ajax_load_cfg'),
    path(
        'ajax/load-event-types/',
        load_event_type,
        name='ajax_load_event_types'
    ),
    path(
        'ajax/load-request-cfg-cam/',
        load_cameras_in_request,
        name='ajax_load_cfg_cam'
    ),
    path(
        'ajax/load-request-cfg-optic/',
        load_optics_in_request,
        name='ajax_load_cfg_optic'
    ),
    path(
        'ajax/load-request-cfg-server/',
        load_servers_in_request,
        name='ajax_load_cfg_server'
    ),
    path(
        'ajax/load-request-cfg-gfx/',
        load_gfx_in_request,
        name='ajax_load_cfg_gfx'
    ),
    path(
        'ajax/load-request-cfg-micro/',
        load_micro_in_request,
        name='ajax_load_cfg_micro'
    ),
    path('print/', printbtk, name='printbtk'),
]
 #path('create/<int:pk>/', PtsRequestEdit.as_view(), name='request_edit'),