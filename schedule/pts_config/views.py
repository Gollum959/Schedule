from typing import Any, Dict
from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView,
                                  TemplateView)
from django.urls import reverse_lazy
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict


from place_broadcast.models import PlaceCity
from pts_config.models import (PtsConstructor,
                               CameraModelBrend,
                               CameraPtsConstructor,
                               OpticModelBrend,
                               OpticPtsConstructor,
                               ServerRecordingRepeatModelBrend,
                               ServerRecordingRepeatConstructor,
                               GfxPtsConstructor,
                               MicrophoneModelBrend)
from pts_config.forms import (AddPtsConfigFrom,
                              AddPtsConfigOnBaseFrom,
                              AddCamera,
                              AddOptic,
                              AddServer,
                              AddGfx,
                              CameraFormset,
                              OpticFormset,
                              ServerFormset,
                              GfxFormset)
from core.custom_view import (DetalInformationMixin,
                              CreateOnlyMainDirectorMixin)


class PtsConfigMainPage(LoginRequiredMixin, TemplateView):
    """PTS configuration main page."""

    login_url = reverse_lazy('users:login')
    template_name = "pts_config/config_main.html"

    def get_context_data(self, **kwargs):
        """Add cities to context."""
        context = super().get_context_data(**kwargs)
        context['cities'] = PlaceCity.objects.all()
        return context


class PtsConfigView(LoginRequiredMixin, ListView):
    """PTS configs list view."""

    login_url = reverse_lazy('users:login')
    model = PtsConstructor
    template_name = 'pts_config/list_config.html'

    def get_queryset(self):
        """Filters PtsConstructor objects."""

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

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Add place_id, event_type_id  to context."""

        data = super().get_context_data(**kwargs)
        place_id = self.request.GET.get('place_id', None)
        event_type_id = self.request.GET.get('event_type_id', None)
        if place_id and event_type_id:
            data['place_id'] = place_id
            data['event_type_id'] = event_type_id

        return data


class PtsConfigDetail(DetalInformationMixin, LoginRequiredMixin, DetailView):
    """PTS config detail view"""
    login_url = reverse_lazy('users:login')
    model = PtsConstructor
    template_name = 'pts_config/config_detail.html'


class PtsBaseConfigCreate(CreateOnlyMainDirectorMixin, CreateView):
    """CreateView class to create a basic configuration"""

    BASE_CFG = True
    form_class = AddPtsConfigFrom
    model = PtsConstructor
    template_name = 'pts_config/create_config.html'

    def get_form_kwargs(self):
        """Adds attributes(place, event) to form's kwargs."""

        kwargs = super().get_form_kwargs()
        kwargs.update({'place': self.request.GET.get('place')})
        kwargs.update({'event': self.request.GET.get('event')})
        return kwargs

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Add to context inlineformset_factories"""

        data = super().get_context_data(**kwargs)
        pts_cfg = {
            'camera': CameraFormset,
            'optic': OpticFormset,
            'server': ServerFormset,
            'gfx': GfxFormset,
        }
        if self.request.POST:
            for context_key, form in pts_cfg.items():
                data[context_key] = form(self.request.POST)
        else:
            for context_key, form in pts_cfg.items():
                data[context_key] = form()
        data['city_name'] = PlaceCity.objects.get(
            placeconstructor__pk=self.request.GET.get('place')
        )

        return data

    def form_valid(self, form):
        """Saves the new object and all inlineformset_factories"""

        form.instance.author = self.request.user
        form.instance.base_conf = self.BASE_CFG
        context = self.get_context_data()
        pts_cfg_forms = [context['camera'], context['optic'],
                         context['server'], context['gfx'],]
        if all([inline_form.is_valid() for inline_form in pts_cfg_forms]):
            self.object = form.save()
            for cfg_form in pts_cfg_forms:
                cfg_form.instance = self.object
                cfg_form.save()
        else:
            return self.render_to_response(self.get_context_data(form=form))

        return HttpResponseRedirect(self.get_success_url())


class PtsConfigCreateOnBase(LoginRequiredMixin, CreateView):
    """CreateView class to create a configuration based on a base"""

    BASE_CFG = False
    login_url = reverse_lazy('users:login')
    form_class = AddPtsConfigOnBaseFrom
    model = PtsConstructor
    template_name = 'pts_config/create_config_onbase.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Add to context cleared data from inlineformset_factories"""

        data = super().get_context_data(**kwargs)
        pts_cfg = {
            'camera': CameraFormset,
            'optic': OpticFormset,
            'server': ServerFormset,
            'gfx': GfxFormset,
        }
        pts_form_fill_cfg = {
            'camera': {
                'formset_model': CameraPtsConstructor,
                'formset_form': AddCamera
            },
            'optic': {
                'formset_model': OpticPtsConstructor,
                'formset_form': AddOptic
            },
            'server': {
                'formset_model': ServerRecordingRepeatConstructor,
                'formset_form': AddServer
            },
            'gfx': {
                'formset_model': GfxPtsConstructor,
                'formset_form': AddGfx
            },
        }
        base_object = get_object_or_404(PtsConstructor, pk=self.kwargs['pk'])
        if self.request.POST:
            for context_key, form in pts_cfg.items():
                data[context_key] = form(self.request.POST)
        else:
            self.object = base_object
            self.object.pk = None

            for context_key, form in pts_form_fill_cfg.items():
                cfg_objects = form['formset_model'].objects.filter(
                    constructor=self.kwargs['pk'])
                cfg_objects_listofdict = []
                for cfg_object in cfg_objects:
                    cfg_object_dict = model_to_dict(cfg_object)
                    del cfg_object_dict['id']
                    del cfg_object_dict['constructor']
                    cfg_objects_listofdict.append(cfg_object_dict)

                CfgObjectBaseFormset = forms.inlineformset_factory(
                    PtsConstructor, form['formset_model'],
                    form=form['formset_form'],
                    extra=len(cfg_objects_listofdict),
                    can_delete=True
                )
                data[context_key] = CfgObjectBaseFormset(
                    instance=self.object, initial=cfg_objects_listofdict)

            data['form'] = AddPtsConfigFrom(instance=self.object)

        data['cfg_info'] = base_object
        return data

    def get_form_kwargs(self):
        """Adds user to form's kwargs."""

        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        """Saves the new object and all inlineformset_factories"""

        context = self.get_context_data()
        if not form.cleaned_data.get('image'):
            form.instance.image = context.get('cfg_info').image
        form.instance.event_type = context.get('cfg_info').event_type
        form.instance.place = context.get('cfg_info').place
        form.instance.author = self.request.user
        form.instance.base_conf = self.BASE_CFG
        pts_cfg_forms = [context['camera'], context['optic'],
                         context['server'], context['gfx'],]
        if all([inline_form.is_valid() for inline_form in pts_cfg_forms]):
            self.object = form.save()
            for cfg_form in pts_cfg_forms:
                cfg_form.instance = self.object
                cfg_form.save()
        else:
            return self.render_to_response(self.get_context_data(form=form))

        return HttpResponseRedirect(self.get_success_url())


class PtsConfigEdit(LoginRequiredMixin, UpdateView):

    login_url = reverse_lazy('users:login')
    form_class = AddPtsConfigFrom
    model = PtsConstructor
    template_name = 'pts_config/create_config.html'

    def get_object(self, *args, **kwargs):
        """Only author or admin can edit the base configuration"""

        obj = super().get_object(*args, **kwargs)
        if obj.author != self.request.user and not self.request.user.is_admin:
            raise PermissionDenied()
        return obj

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Add to context inlineformset_factories"""

        data = super().get_context_data(**kwargs)
        pts_cfg = {
            'camera': CameraFormset,
            'optic': OpticFormset,
            'server': ServerFormset,
            'gfx': GfxFormset,
        }
        if self.request.POST:
            for context_key, form in pts_cfg.items():
                data[context_key] = form(self.request.POST,
                                         instance=self.object)
        else:
            for context_key, form in pts_cfg.items():
                data[context_key] = form(instance=self.object)

        data['city_name'] = self.object.place.city_name

        return data

    def form_valid(self, form):

        form.instance.author = self.request.user
        context = self.get_context_data()
        pts_cfg_forms = [context['camera'], context['optic'],
                         context['server'], context['gfx'],]

        if all([inline_form.is_valid() for inline_form in pts_cfg_forms]):
            self.object = form.save()
            for cfg_form in pts_cfg_forms:
                cfg_form.instance = self.object
                cfg_form.save()
        else:
            return self.render_to_response(self.get_context_data(form=form))

        return HttpResponseRedirect(self.get_success_url())


class PtsConfigDelete(LoginRequiredMixin, DeleteView):
    """View class for delete PTS configuration."""

    model = PtsConstructor
    template_name = 'pts_config/list_config.html'
    success_url = reverse_lazy('config:pts_configs')

    def get_object(self, *args, **kwargs):
        """Only author or admin can delete the base configuration"""
        user = self.request.user
        obj = super().get_object(*args, **kwargs)
        if not (obj.author == user or user.is_admin):
            raise PermissionDenied
        return obj


def load_camera_brend(request):
    camera_brend_id = request.GET.get('brend')
    camera_id = request.GET.get('camera')
    camera_models = []
    if camera_brend_id:
        camera_models = CameraModelBrend.objects.filter(
            brend=camera_brend_id, type=camera_id).order_by('name')
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
