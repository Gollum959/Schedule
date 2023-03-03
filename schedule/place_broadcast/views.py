from typing import Any, Dict
from django.db import IntegrityError
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy

from place_broadcast.forms import AddBroadcastPlace
from place_broadcast.models import PlaceConstructor, PlaceCity
from core.custom_view import DetalInformationMixin, EditOnlyAuthorMixin


class CityBroadcastCreate(LoginRequiredMixin, CreateView):

    login_url = reverse_lazy('users:login')
    model = PlaceCity
    fields = ('name', )
    template_name = 'place_broadcast/create_city.html'

    def form_valid(self, form):
        instance = form.save()
        return HttpResponse(
            f'<script>opener.closePopup(window, '
            f'"{instance.pk}", "{instance}", "#id_city_name");</script>'
        )


class CitiesBroadcastView(LoginRequiredMixin, ListView):
    """User places templates list view"""
    login_url = reverse_lazy('users:login')
    model = PlaceCity
    template_name = 'place_broadcast/list_cities.html'

    # def get_queryset(self):
    #     return PlaceConstructor.objects.filter(author=self.request.user)


class PlacesBroadcastView(LoginRequiredMixin, ListView):
    """User places templates list view"""
    login_url = reverse_lazy('users:login')
    model = PlaceConstructor
    template_name = 'place_broadcast/list_places.html'

    def get_queryset(self):
        requests = PlaceConstructor.objects.none()
        city_id = self.request.GET.get('city_id', None)
        if city_id:
            requests = PlaceConstructor.objects.filter(city_name=city_id)

        return requests

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        data = super().get_context_data(**kwargs)
        data['city_id'] = self.request.GET.get('city_id', None)

        return data
    # def get_queryset(self):
    #     return PlaceConstructor.objects.filter(author=self.request.user)


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

    def get_form_kwargs(self):
        kwargs = super(PlacesBroadcastCreate, self).get_form_kwargs()
        kwargs.update({'city_id': self.request.GET.get('city_id')})
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PlacesBroadcastEdit(EditOnlyAuthorMixin, LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('users:login')
    form_class = AddBroadcastPlace
    model = PlaceConstructor
    template_name = 'place_broadcast/create_places.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
