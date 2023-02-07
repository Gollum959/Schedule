from django.urls import path
from pts_requests.views import (
    PtsRequestsView, PtsRequestDetail, PtsRequestCreate,
    PtsRequestEdit
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
]
