from django.urls import path
from pts_requests.views import (
    PtsRequestsView, PtsRequestDetail, PtsRequestCreate,
    PtsRequestEdit, PtsRequestModerate, load_places, load_pts_cfg,
    load_event_type, change_status_to_on_approval, remove_draft_pts_request
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
]
