from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy

from place_broadcast.forms import AddBroadcastPlace
from place_broadcast.models import PlaceConstructor
from core.custom_view import DetalInformationMixin


class PlacesBroadcastView(LoginRequiredMixin, ListView):
    """User places templates list view"""
    login_url = reverse_lazy('users:login')
    model = PlaceConstructor
    template_name = 'place_broadcast/list_places.html'

    def get_queryset(self):
        return PlaceConstructor.objects.filter(author=self.request.user)


class PlacesBroadcastDetail(
    DetalInformationMixin, LoginRequiredMixin, DetailView
):
    """Place detail view"""
    login_url = reverse_lazy('users:login')
    model = PlaceConstructor
    template_name = 'place_broadcast/place_detail.html'


class PlacesBroadcastCreate(LoginRequiredMixin, CreateView):
    """Create new broadcast place"""

    login_url = reverse_lazy('users:login')
    form_class = AddBroadcastPlace
    template_name = 'place_broadcast/create_places.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        self.object = form.save()
        return super().form_valid(form)


class PlacesBroadcastEdit:
    ...
