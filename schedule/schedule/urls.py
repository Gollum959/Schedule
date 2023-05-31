from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('', include('pts_requests.urls', namespace='pts_requests')),
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls', namespace='users')),
    path('place/', include('place_broadcast.urls', namespace='place')),
    path('config/', include('pts_config.urls', namespace='config')),
    path('api/', include('api.urls')),
]
