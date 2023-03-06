from django.urls import path
from pts_config.views import (
                              PtsConfigView,
                              PtsConfigDetail,
                              PtsBaseConfigCreate,
                              PtsBaseConfigEdit,
                              PtsConfigMainPage,
                              PtsConfigCreateOnBase,
                              load_camera_brend,
                              load_optic_brend,
                              load_server_brend,
                              load_micro_brend)

app_name = 'pts_config'

urlpatterns = [
    path('', PtsConfigMainPage.as_view(), name='pts_configs'),
    path(
        '<int:pk>/',
        PtsConfigDetail.as_view(),
        name='config_detail'
    ),
    path(
        'create/',
        PtsBaseConfigCreate.as_view(),
        name='config_create'
    ),
    path(
        'create/<int:pk>/',
        PtsBaseConfigEdit.as_view(),
        name='config_edit',
    ),
    path(
        'createonbase/<int:pk>/',
        PtsConfigCreateOnBase.as_view(),
        name='config_create_onbase',
    ),
    path(
        'ajax/load-cam-model/',
        load_camera_brend,
        name='ajax_load_cam_model'
    ),
    path(
        'ajax/load-optic-model/',
        load_optic_brend,
        name='ajax_load_optic_model'
    ),
    path(
        'ajax/load-server-model/',
        load_server_brend,
        name='ajax_load_server_model'
    ),
    path(
        'ajax/load-micro-model/',
        load_micro_brend,
        name='ajax_load_micro_model'
    ),
    path(
        'ajax/load-place_cfg/',
        PtsConfigView.as_view(),
        name='ajax_load_cfg'
    ),
]
