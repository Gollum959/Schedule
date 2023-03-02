from typing import Any, Dict
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView,
                                  TemplateView)
from django.urls import reverse_lazy
from django.db.models import Q


from place_broadcast.models import PlaceCity
from pts_config.models import (PtsConstructor,
                               CameraModelBrend,
                               OpticModelBrend,
                               ServerRecordingRepeatModelBrend,
                               MicrophoneModelBrend)
from pts_config.forms import (AddPtsConfigFrom,
                              CameraFormset,
                              OpticFormset,
                              ServerFormset,
                              MicroFormset,
                              GfxFormset)
from core.custom_view import DetalInformationMixin, EditOnlyAuthorMixin


class PtsConfigView(LoginRequiredMixin, ListView):
    """User PTS configs list view"""
    login_url = reverse_lazy('users:login')
    model = PtsConstructor
    template_name = 'pts_config/list_config.html'

    def get_queryset(self):
        requests = PtsConstructor.objects.none()
        place_id = self.request.GET.get('place_id', None)
        event_type_id = self.request.GET.get('event_type_id', None)
        if place_id and event_type_id:
            requests = PtsConstructor.objects.filter(
                place=place_id,
                event_type=event_type_id,
                clone_conf=False
            ).filter(
                Q(author=self.request.user) | Q(base_conf=True)
            ).order_by('-base_conf', 'name')

        return requests


class PtsConfigMainPage(LoginRequiredMixin, TemplateView):

    login_url = reverse_lazy('users:login')
    template_name = "pts_config/config_main.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cities'] = PlaceCity.objects.all()
        return context


class PtsConfigDetail(DetalInformationMixin, LoginRequiredMixin, DetailView):
    """PTS config detail view"""
    login_url = reverse_lazy('users:login')
    model = PtsConstructor
    template_name = 'pts_config/config_detail.html'


class PtsConfigCreate(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('users:login')
    form_class = AddPtsConfigFrom
    model = PtsConstructor
    template_name = 'pts_config/create_config.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        data = super().get_context_data(**kwargs)
        pts_cfg = {
            'camera': CameraFormset,
            'optic': OpticFormset,
            'server': ServerFormset,
            'micro': MicroFormset,
            'gfx': GfxFormset,
        }
        if self.request.POST:
            for context_key, form in pts_cfg.items():
                data[context_key] = form(self.request.POST)
        else:
            for context_key, form in pts_cfg.items():
                data[context_key] = form()

        return data

    def form_valid(self, form):
        form.instance.author = self.request.user
        context = self.get_context_data()
        pts_cfg_forms = [context['camera'], context['optic'],
                         context['server'], context['micro'],
                         context['gfx'],]
        self.object = form.save()
        for cfg_form in pts_cfg_forms:
            if cfg_form.is_valid():
                cfg_form.instance = self.object
                cfg_form.save()

        return super().form_valid(form)


class PtsConfigEdit(EditOnlyAuthorMixin, LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('users:login')
    form_class = AddPtsConfigFrom
    model = PtsConstructor
    template_name = 'pts_config/create_config.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        data = super().get_context_data(**kwargs)
        pts_cfg = {
            'camera': CameraFormset,
            'optic': OpticFormset,
            'server': ServerFormset,
            'micro': MicroFormset,
            'gfx': GfxFormset,
        }
        if self.request.POST:
            for context_key, form in pts_cfg.items():
                data[context_key] = form(self.request.POST,
                                         instance=self.object)
        else:
            for context_key, form in pts_cfg.items():
                data[context_key] = form(instance=self.object)

        return data

    def form_valid(self, form):
        form.instance.author = self.request.user
        context = self.get_context_data()
        pts_cfg_forms = [context['camera'], context['optic'],
                         context['server'], context['micro'],
                         context['gfx'],]
        self.object = form.save()

        for cfg_form in pts_cfg_forms:
            if cfg_form.is_valid():
                cfg_form.instance = self.object
                cfg_form.save()

        return super().form_valid(form)


def load_camera_brend(request):
    camera_brend_id = request.GET.get('id')
    camera_models = CameraModelBrend.objects.filter(
        brend=camera_brend_id).order_by('name')
    return render(
        request,
        'pts_config/camera_model_dropdown_list_options.html',
        {'camera_models': camera_models}
    )


def load_optic_brend(request):
    optic_brend_id = request.GET.get('id')
    optic_models = OpticModelBrend.objects.filter(
        brend=optic_brend_id).order_by('name')
    return render(
        request,
        'pts_config/optic_model_dropdown_list_options.html',
        {'optic_models': optic_models}
    )


def load_server_brend(request):
    server_brend_id = request.GET.get('id')
    server_models = ServerRecordingRepeatModelBrend.objects.filter(
        brend=server_brend_id).order_by('name')
    return render(
        request,
        'pts_config/server_model_dropdown_list_options.html',
        {'server_models': server_models}
    )


def load_micro_brend(request):
    micro_brend_id = request.GET.get('id')
    micro_models = MicrophoneModelBrend.objects.filter(
        brend=micro_brend_id).order_by('name')
    return render(
        request,
        'pts_config/micro_model_dropdown_list_options.html',
        {'micro_models': micro_models}
    )
