from django.contrib import admin
from django.urls import include, path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static

schema_view = get_schema_view(
    openapi.Info(
        title='API Documentation',
        default_version='v1',
    ),
    public=True,
)

urlpatterns = [
    path('', include('pts_requests.urls', namespace='pts_requests')),
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls', namespace='users')),
    path('place/', include('place_broadcast.urls', namespace='place')),
    path('config/', include('pts_config.urls', namespace='config')),
    path('api/', include('api.urls')),
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0)),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
