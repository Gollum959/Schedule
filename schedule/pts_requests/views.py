from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.urls import reverse_lazy

from pts_requests.models import PtsRequest
from core.custom_view import DetailViewOnlyAuthor


class PtsRequestsView(LoginRequiredMixin, ListView):
    """Requets list view"""
    login_url = reverse_lazy('users:login')
    model = PtsRequest
    template_name = 'pts_requests/list_requests.html'

    def get_queryset(self):
        if self.request.user.is_admin or self.request.user.is_moderator:
            return PtsRequest.objects.all()
        return PtsRequest.objects.filter(author=self.request.user)


class PtsRequestDetail(DetailViewOnlyAuthor):
    """Request detail view"""
    login_url = reverse_lazy('users:login')
    model = PtsRequest
    template_name = 'pts_requests/request_detail.html'
