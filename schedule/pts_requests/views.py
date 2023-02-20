from datetime import date, timedelta, datetime
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from typing import Any, Dict

from place_broadcast.models import PlaceConstructor, EventType
from pts_requests.models import PtsRequest
from pts_requests.forms import (AddRequestFrom,
                                ModerateRequestFrom,
                                CommLineFormset,
                                TechCommLineFormset)
from core.custom_view import (DetalInformationMixin,
                              UserToFormMixin,
                              EditOnlyAuthorMixin)


class PtsRequestsView(LoginRequiredMixin, ListView):
    """Requets list view"""
    login_url = reverse_lazy('users:login')
    model = PtsRequest
    template_name = 'pts_requests/list_requests.html'

    def get_queryset(self):
        requests = PtsRequest.objects.all()
        today = date.today()
        start_week = today - timedelta(days=today.weekday())
        end_week = start_week + timedelta(days=6)

        if self.request.GET.get('week') == 'next':
            start_week = start_week + timedelta(days=7)
            end_week = start_week + timedelta(days=6)

        format = '%Y-%m-%d'
        try:
            res = bool(datetime.strptime(
                self.request.GET.get('date', ''), format)
            )
        except ValueError:
            res = False

        if res:
            requests = requests.filter(
                broadcast_start_date__date=self.request.GET.get('date')
            )
        else:
            requests = requests.filter(
                broadcast_start_date__range=[start_week, end_week]
            )

        if self.request.user.is_admin or self.request.user.is_moderator:
            return requests

        return requests.filter(author=self.request.user)


class PtsRequestDetail(DetalInformationMixin, LoginRequiredMixin, DetailView):
    """Request detail view"""
    login_url = reverse_lazy('users:login')
    model = PtsRequest
    template_name = 'pts_requests/request_detail.html'

    # def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
    #     data = super().get_context_data(**kwargs)
    #     data['trakt'] = (
    #         data['object'].broadcast_start_date - timedelta(hours=1)
    #     )
    #     return data


class PtsRequestCreate(UserToFormMixin, LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('users:login')
    form_class = AddRequestFrom
    model = PtsRequest
    template_name = 'pts_requests/create_requests.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        data = super().get_context_data(**kwargs)

        if self.request.POST:
            data['commline'] = CommLineFormset(self.request.POST)
            data['techcommline'] = TechCommLineFormset(self.request.POST)
        else:
            data['commline'] = CommLineFormset()
            data['techcommline'] = TechCommLineFormset()

        return data

    def form_valid(self, form):
        form.instance.author = self.request.user
        context = self.get_context_data()
        commlines = context['commline']
        techcommlines = context['techcommline']
        self.object = form.save()

        if commlines.is_valid():
            commlines.instance = self.object
            commlines.save()
        if techcommlines.is_valid():
            techcommlines.instance = self.object
            techcommlines.save()

        return super().form_valid(form)


class PtsRequestEdit(UserToFormMixin, EditOnlyAuthorMixin,
                     LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('users:login')
    form_class = AddRequestFrom
    model = PtsRequest
    template_name = 'pts_requests/create_requests.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        data = super().get_context_data(**kwargs)

        if self.request.POST:
            data['commline'] = CommLineFormset(
                self.request.POST, instance=self.object
            )
            data['techcommline'] = TechCommLineFormset(
                self.request.POST, instance=self.object
            )
        else:
            data['commline'] = CommLineFormset(instance=self.object)
            data['techcommline'] = TechCommLineFormset(instance=self.object)

        return data

    def form_valid(self, form):
        form.instance.author = self.request.user
        context = self.get_context_data()
        commlines = context['commline']
        techcommlines = context['techcommline']
        self.object = form.save()

        if commlines.is_valid():
            commlines.instance = self.object
            commlines.save()
        if techcommlines.is_valid():
            techcommlines.instance = self.object
            techcommlines.save()

        return super().form_valid(form)


class PtsRequestModerate(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('users:login')
    form_class = ModerateRequestFrom
    model = PtsRequest
    template_name = 'pts_requests/request_detail2.html'

    def get_initial(self):
        initial = super(PtsRequestModerate, self).get_initial()
        if not self.object.trakt_start_date:
            initial['trakt_start_date'] = (
                self.object.broadcast_start_date - timedelta(hours=1)
            )
        if not self.object.trakt_end_date:
            initial['trakt_end_date'] = (
                self.object.broadcast_end_date - timedelta(hours=0, minutes=15)
            )
        return initial


def load_places(request):
    city_id = request.GET.get('city_name')
    if city_id:
        places = PlaceConstructor.objects.filter(
            city_name=city_id,
            author__direction=request.user.direction).order_by('name')
    else:
        places = PlaceConstructor.objects.none()
    return render(
        request,
        'pts_requests/place_dropdown_list_options.html',
        {'places': places}
    )


def load_event_type(request):
    place_id = request.GET.get('place')
    if place_id:
        event_types = EventType.objects.filter(
            placeconstructor__pk=place_id).order_by('name')
    else:
        event_types = EventType.objects.none()
    return render(
        request,
        'pts_requests/event_type_dropdown_list_options.html',
        {'event_types': event_types}
    )
