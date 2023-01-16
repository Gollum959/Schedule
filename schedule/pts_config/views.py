from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.urls import reverse_lazy

from pts_config.models import PtsConstructor
from core.custom_view import DetailViewOnlyAuthor


class PtsConfigView(LoginRequiredMixin, ListView):
    """User PTS configs list view"""
    login_url = reverse_lazy('users:login')
    model = PtsConstructor
    template_name = 'pts_config/list_config.html'

    def get_queryset(self):
        return PtsConstructor.objects.filter(author=self.request.user)


class PtsConfigDetail(DetailViewOnlyAuthor):
    """PTS config detail view"""
    login_url = reverse_lazy('users:login')
    model = PtsConstructor
    template_name = 'pts_config/config_detail.html'
