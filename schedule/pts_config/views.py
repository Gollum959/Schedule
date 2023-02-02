from typing import Any, Dict
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy

from pts_config.models import PtsConstructor
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
        return PtsConstructor.objects.filter(author=self.request.user)


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
