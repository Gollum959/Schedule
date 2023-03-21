from datetime import date, timedelta, datetime
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from typing import Any, Dict
from django.http import HttpResponseRedirect

from place_broadcast.models import PlaceConstructor, EventType
from pts_requests.models import PtsRequest
from pts_config.models import PtsConstructor
from pts_requests.forms import (AddRequestFrom,
                                ModerateRequestFrom,
                                UpdateTraktTime,
                                CommLineFormset,
                                TechCommLineFormset,
                                InternetLineFormset)
from pts_config.forms import (CameraModerateFormset,
                              OpticModerateFormset,
                              ServerModerateFormset,
                              GfxModerateFormset)
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
        end_week = start_week + timedelta(days=7)

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

        if self.request.user.is_admin:
            return requests

        requests = requests.filter(
            author__direction=self.request.user.direction
        )
        if self.request.user.is_main_director:
            return requests

        if self.request.user.is_director:
            return requests.filter(~Q(
                ~Q(author=self.request.user)
                & Q(Q(status='draft') | Q(status='rejected'))))

        # return requests.filter(~Q(
        #   ~Q(author=self.request.user) & Q(status='draft')))
        # return requests
        # if self.request.user.is_admin or self.request.user.is_moderator:
        #     return requests
        # return requests.filter(~Q(author=self.request.user and status))


class PtsRequestDetail(DetalInformationMixin, LoginRequiredMixin, DetailView):
    """Request detail view"""
    login_url = reverse_lazy('users:login')
    model = PtsRequest
    template_name = 'pts_requests/request_detail.html'

    def __initial_time(self, time_field, broadcast_time):
        if not time_field:
            time_field = broadcast_time - timedelta(hours=1)
        return time_field

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        data = super().get_context_data(**kwargs)
        initial_dict = {
            'trakt_start_date': self.__initial_time(
                self.object.trakt_start_date,
                self.object.broadcast_start_date),
            'trakt_end_date': self.__initial_time(
                self.object.trakt_end_date,
                self.object.broadcast_end_date)
        }
        data['trakt'] = UpdateTraktTime(
            instance=self.object,
            initial=initial_dict
        )
        return data


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
            data['internetline'] = InternetLineFormset(self.request.POST)
        else:
            data['commline'] = CommLineFormset()
            data['techcommline'] = TechCommLineFormset()
            data['internetline'] = InternetLineFormset()

        return data

    def form_valid(self, form):
        form.instance.author = self.request.user
        context = self.get_context_data()
        commlines = context['commline']
        techcommlines = context['techcommline']
        internetlines = context['internetline']
        if (
            commlines.is_valid() and
            techcommlines.is_valid() and
            internetlines.is_valid()
        ):
            self.object = form.save()
            commlines.instance = self.object
            commlines.save()
            techcommlines.instance = self.object
            techcommlines.save()
            internetlines.instance = self.object
            internetlines.save()
        else:
            return self.render_to_response(self.get_context_data(form=form))

        return HttpResponseRedirect(self.get_success_url())


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
            data['internetline'] = InternetLineFormset(
                self.request.POST, instance=self.object
            )
        else:
            data['commline'] = CommLineFormset(instance=self.object)
            data['techcommline'] = TechCommLineFormset(instance=self.object)
            data['internetline'] = InternetLineFormset(instance=self.object)

        return data

    def form_valid(self, form):
        context = self.get_context_data()
        commlines = context['commline']
        techcommlines = context['techcommline']
        internetlines = context['internetline']
        if (
            commlines.is_valid() and
            techcommlines.is_valid() and
            internetlines.is_valid()
        ):
            self.object = form.save()
            commlines.instance = self.object
            commlines.save()
            techcommlines.instance = self.object
            techcommlines.save()
            internetlines.instance = self.object
            internetlines.save()
        else:
            return self.render_to_response(self.get_context_data(form=form))

        return HttpResponseRedirect(self.get_success_url())
        # if commlines.is_valid():
        #     commlines.instance = self.object
        #     commlines.save()
        # if techcommlines.is_valid():
        #     techcommlines.instance = self.object
        #     techcommlines.save()

        # return super().form_valid(form)


@login_required
def change_status_to_on_approval(request, pk):
    """Change PTS request status from draft to on approval."""
    pts_request = get_object_or_404(PtsRequest, pk=pk)
    if pts_request.author != request.user:
        raise Http404()
    pts_request.status = 'approval'
    pts_request.save()
    return redirect('pts_requests:request_detail', pk=pts_request.pk)


@login_required
def remove_draft_pts_request(request, pk):
    """Remove draft PTS request, only author."""
    pts_request = get_object_or_404(PtsRequest, pk=pk)
    if pts_request.author != request.user and not pts_request.is_draft:
        raise Http404()
    pts_request.delete()
    return redirect('pts_requests:index')


@login_required
def load_places(request):
    city_id = request.GET.get('city_name')
    if city_id:
        places = PlaceConstructor.objects.filter(
            city_name=city_id, ).order_by('name')
        # author__direction=request.user.direction).order_by('name')
    else:
        places = PlaceConstructor.objects.none()
    return render(
        request,
        'pts_requests/place_dropdown_list_options.html',
        {'places': places}
    )


@login_required
def load_event_type(request):
    place_id = request.GET.get('place_id')
    if place_id:
        event_types = EventType.objects.filter(
            placeconstructor__pk=place_id,
            direction=request.user.direction
        ).order_by('name')
    else:
        event_types = EventType.objects.none()
    return render(
        request,
        'pts_requests/event_type_dropdown_list_options.html',
        {'event_types': event_types}
    )


@login_required
def load_pts_cfg(request):
    event_id = request.GET.get('event_id')
    place_id = request.GET.get('place_id')
    if event_id:
        cfgs = PtsConstructor.objects.filter(
            place=place_id, event_type=event_id, clone_conf=False).filter(
            Q(author=request.user) | Q(base_conf=True)).order_by('name')
    else:
        cfgs = PtsConstructor.objects.none()
    return render(
        request,
        'pts_requests/cfg_dropdown_list_options.html',
        {'cfgs': cfgs}
    )


@login_required
def load_cameras_in_request(request):

    request_id = request.GET.get('requestId')
    pts_request = get_object_or_404(PtsRequest, pk=request_id)
    camera_form = CameraModerateFormset(instance=pts_request.pts_cfg)
    return render(
        request,
        'pts_requests/request_cfg_cameras.html',
        {'camera_form': camera_form}
    )


@login_required
def load_optics_in_request(request):

    request_id = request.GET.get('requestId')
    pts_request = get_object_or_404(PtsRequest, pk=request_id)
    optic_form = OpticModerateFormset(instance=pts_request.pts_cfg)
    return render(
        request,
        'pts_requests/request_cfg_optics.html',
        {'optic_form': optic_form}
    )


@login_required
def load_servers_in_request(request):

    request_id = request.GET.get('requestId')
    pts_request = get_object_or_404(PtsRequest, pk=request_id)
    server_form = ServerModerateFormset(instance=pts_request.pts_cfg)
    return render(
        request,
        'pts_requests/request_cfg_servers.html',
        {'server_form': server_form}
    )


@login_required
def load_gfx_in_request(request):

    request_id = request.GET.get('requestId')
    pts_request = get_object_or_404(PtsRequest, pk=request_id)
    gfx_form = GfxModerateFormset(instance=pts_request.pts_cfg)
    return render(
        request,
        'pts_requests/request_cfg_gfx.html',
        {'gfx_form': gfx_form}
    )


@login_required
def load_micro_in_request(request):
    request_id = request.GET.get('requestId')
    pts_request = get_object_or_404(PtsRequest, pk=request_id)

    return render(
        request,
        'pts_requests/request_cfg_micro.html',
        {'quantity': pts_request.pts_cfg.microphone_quantity}
    )

# Forms for time block


class PtsRequestModerate(LoginRequiredMixin, UpdateView): # need add moderator role permission
    login_url = reverse_lazy('users:login')
    form_class = ModerateRequestFrom
    model = PtsRequest
    template_name = 'pts_requests/request_detail2.html'

    def get_initial(self):
        initial = super().get_initial()
        if not self.object.trakt_start_date:
            initial['trakt_start_date'] = (
                self.object.broadcast_start_date - timedelta(hours=1)
            )
        if not self.object.trakt_end_date:
            initial['trakt_end_date'] = (
                self.object.broadcast_end_date - timedelta(hours=0, minutes=15)
            )
        return initial