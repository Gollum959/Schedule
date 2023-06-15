from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from pts_config.models import CameraModelBrend, OpticModelBrend


class CameraDjangoFilterBackend(DjangoFilterBackend):
    def filter_queryset(self, request, queryset, view):
        queryset = CameraModelBrend.objects.all()
        brend_type_pts = request.query_params.get('brend__type_pts')
        type_cam = request.query_params.get('type')
        brend = request.query_params.get('brend')
        if brend_type_pts:
            queryset = queryset.filter(
                Q(brend__type_pts=brend_type_pts) |
                Q(brend__type_pts__isnull=True))
        if type_cam:
            queryset = queryset.filter(type__pk=type_cam)
        if brend:
            queryset = queryset.filter(brend__pk=brend)
        return queryset


class OpticDjangoFilterBackend(DjangoFilterBackend):
    def filter_queryset(self, request, queryset, view):
        queryset = OpticModelBrend.objects.all()
        brend_type_pts = request.query_params.get('brend__type_pts')
        type_name = request.query_params.get('type__name')
        if brend_type_pts:
            queryset = queryset.filter(
                Q(brend__type_pts=brend_type_pts) |
                Q(brend__type_pts__isnull=True))
        if type_name:
            queryset = queryset.filter(type__name=type_name)
        return queryset
