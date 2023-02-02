from django.urls import path
from pts_config.views import (PtsConfigView,
                              PtsConfigDetail,
                              PtsConfigCreate,
                              PtsConfigEdit)

app_name = 'pts_config'

urlpatterns = [
    path('', PtsConfigView.as_view(), name='pts_configs'),
    path(
        '<int:pk>/',
        PtsConfigDetail.as_view(),
        name='config_detail'
    ),
    path(
        'create/',
        PtsConfigCreate.as_view(),
        name='config_create'
    ),
    path('create/<int:pk>/', PtsConfigEdit.as_view(), name='config_edit'),
]
