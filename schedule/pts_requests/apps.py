from django.apps import AppConfig


class PtsRequestsConfig(AppConfig):
    name = 'pts_requests'

    def ready(self):
        from pts_requests import signals
