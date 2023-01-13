from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy

from place_broadcast.models import PlaceConstructor


class PlacesBroadcastView(LoginRequiredMixin, ListView):
    """User places templates list view"""
    login_url = reverse_lazy('users:login')
    model = PlaceConstructor
    template_name = 'place_broadcast/list_places.html'

    def get_queryset(self):
        return PlaceConstructor.objects.filter(author=self.request.user)


class PlacesBroadcastDetail(LoginRequiredMixin, DetailView):
    """Request detail view"""
    login_url = reverse_lazy('users:login')
    model = PlaceConstructor
    template_name = 'place_broadcast/place_detail.html'
