from django.urls import path
from pts_config.views import PtsConfigView, PtsConfigDetail

app_name = 'pts_config'

urlpatterns = [
    path('', PtsConfigView.as_view(), name='pts_configs'),
    path(
        '<int:pk>/',
        PtsConfigDetail.as_view(),
        name='config_detail'
    ),
]
