from typing import Any, Dict
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
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
                              GfxFormset)
from core.custom_view import (DetalInformationMixin,
                              EditOnlyAuthorMixin,
                              CreateOnlyMainDirectorMixin)


class PtsConfigMainPage(LoginRequiredMixin, TemplateView):

    login_url = reverse_lazy('users:login')
    template_name = "pts_config/config_main.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cities'] = PlaceCity.objects.all()
        return context


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

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
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

    BASE_CFG = True
    form_class = AddPtsConfigFrom
    model = PtsConstructor
    template_name = 'pts_config/create_config.html'
    
    def get_form_kwargs(self):
        kwargs = super(PtsBaseConfigCreate, self).get_form_kwargs()
        kwargs.update({'place': self.request.GET.get('place')})
        kwargs.update({'event': self.request.GET.get('event')})
        return kwargs

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
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
        form.instance.author = self.request.user
        form.instance.base_conf = self.BASE_CFG
        context = self.get_context_data()
        pts_cfg_forms = [context['camera'], context['optic'],
                         context['server'], context['gfx'],]
        print(context['camera'].is_valid())
        if all([inline_form.is_valid() for inline_form in pts_cfg_forms]):
            self.object = form.save()
            for cfg_form in pts_cfg_forms:
                cfg_form.instance = self.object
                cfg_form.save()
        else:
            return self.render_to_response(self.get_context_data(form=form))

        return HttpResponseRedirect(self.get_success_url())
    

class PtsConfigCreateOnBase(PtsBaseConfigCreate):
    
    BASE_CFG = False
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
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
            self.object = PtsConstructor.objects.get(pk=self.kwargs['pk'])
            data['form'] = AddPtsConfigFrom(instance=self.object)
            for context_key, form in pts_cfg.items():
                data[context_key] = form(instance=self.object)
        data['city_name'] = PlaceCity.objects.get(
            placeconstructor__pk=self.request.GET.get('place')
        )

        return data



class PtsBaseConfigEdit(CreateOnlyMainDirectorMixin, UpdateView):
    form_class = AddPtsConfigFrom
    model = PtsConstructor
    template_name = 'pts_config/create_config.html'

    def get_object(self, *args, **kwargs):
        """Only author cat edit the base configuration"""
        obj = super().get_object(*args, **kwargs)
        if obj.author != self.request.user:
            raise PermissionDenied()
        return obj

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
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
        # for cfg_form in pts_cfg_forms:
        #     if cfg_form.is_valid():
        #         cfg_form.instance = self.object
        #         cfg_form.save()

        # return super().form_valid(form)


# class PtsConfigCreate(LoginRequiredMixin, CreateView):
#     login_url = reverse_lazy('users:login')
#     form_class = AddPtsConfigFrom
#     model = PtsConstructor
#     template_name = 'pts_config/create_config.html'

#     def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
#         data = super().get_context_data(**kwargs)
#         pts_cfg = {
#             'camera': CameraFormset,
#             'optic': OpticFormset,
#             'server': ServerFormset,
#             'micro': MicroFormset,
#             'gfx': GfxFormset,
#         }
#         if self.request.POST:
#             for context_key, form in pts_cfg.items():
#                 data[context_key] = form(self.request.POST)
#         else:
#             for context_key, form in pts_cfg.items():
#                 data[context_key] = form()

#         return data

#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         context = self.get_context_data()
#         pts_cfg_forms = [context['camera'], context['optic'],
#                          context['server'], context['micro'],
#                          context['gfx'],]
#         self.object = form.save()
#         for cfg_form in pts_cfg_forms:
#             if cfg_form.is_valid():
#                 cfg_form.instance = self.object
#                 cfg_form.save()

#         return super().form_valid(form)


# class PtsConfigEdit(EditOnlyAuthorMixin, LoginRequiredMixin, UpdateView):
#     login_url = reverse_lazy('users:login')
#     form_class = AddPtsConfigFrom
#     model = PtsConstructor
#     template_name = 'pts_config/create_config.html'

#     def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
#         data = super().get_context_data(**kwargs)
#         pts_cfg = {
#             'camera': CameraFormset,
#             'optic': OpticFormset,
#             'server': ServerFormset,
#             'micro': MicroFormset,
#             'gfx': GfxFormset,
#         }
#         if self.request.POST:
#             for context_key, form in pts_cfg.items():
#                 data[context_key] = form(self.request.POST,
#                                          instance=self.object)
#         else:
#             for context_key, form in pts_cfg.items():
#                 data[context_key] = form(instance=self.object)

#         return data

#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         context = self.get_context_data()
#         pts_cfg_forms = [context['camera'], context['optic'],
#                          context['server'], context['micro'],
#                          context['gfx'],]
#         self.object = form.save()

#         for cfg_form in pts_cfg_forms:
#             if cfg_form.is_valid():
#                 cfg_form.instance = self.object
#                 cfg_form.save()

#         return super().form_valid(form)


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







# {'csrfmiddlewaretoken': ['ZR5fYWFdwgiqZEYItDVSntAz9wubdTaPI1dtA0NNA0s17R0M0mphjSrKEsScGuTr'],
#  'name': ['99999 77777789999067857xvbcvxbxv f gb fg b09'],
#  'image': [''],
#  'cameraptsconstructor_set-TOTAL_FORMS': ['1'],
#  'cameraptsconstructor_set-INITIAL_FORMS': ['1'],
#  'cameraptsconstructor_set-MIN_NUM_FORMS': ['0'],
#  'cameraptsconstructor_set-MAX_NUM_FORMS': ['1000'],
#  'cameraptsconstructor_set-0-cameras': ['1'],
#  'cameraptsconstructor_set-0-quantity': ['2'],
#  'cameraptsconstructor_set-0-id': ['14'],
#  'cameraptsconstructor_set-0-constructor': ['56'],
#  'cameraptsconstructor_set-__prefix__-cameras': [''],
#  'cameraptsconstructor_set-__prefix__-quantity': ['0'],
#  'cameraptsconstructor_set-__prefix__-id': [''],
#  'cameraptsconstructor_set-__prefix__-constructor': ['56'],
  
#  'opticptsconstructor_set-TOTAL_FORMS': ['2'], 'opticptsconstructor_set-INITIAL_FORMS': ['2'], 'opticptsconstructor_set-MIN_NUM_FORMS': ['0'], 'opticptsconstructor_set-MAX_NUM_FORMS': ['1000'], 'opticptsconstructor_set-0-optics': ['2'], 'opticptsconstructor_set-0-quantity': ['2'], 'opticptsconstructor_set-0-id': ['17'], 'opticptsconstructor_set-0-constructor': ['56'], 'opticptsconstructor_set-1-optics': ['6'], 'opticptsconstructor_set-1-quantity': ['2'], 'opticptsconstructor_set-1-id': ['24'], 'opticptsconstructor_set-1-constructor': ['56'], 'opticptsconstructor_set-__prefix__-optics': [''], 'opticptsconstructor_set-__prefix__-quantity': ['0'], 'opticptsconstructor_set-__prefix__-id': [''], 'opticptsconstructor_set-__prefix__-constructor': ['56'], 
# 'serverrecordingrepeatconstructor_set-TOTAL_FORMS': ['1'], 'serverrecordingrepeatconstructor_set-INITIAL_FORMS': ['1'], 'serverrecordingrepeatconstructor_set-MIN_NUM_FORMS': ['0'], 'serverrecordingrepeatconstructor_set-MAX_NUM_FORMS': ['1000'], 'serverrecordingrepeatconstructor_set-0-type': ['1'], 'serverrecordingrepeatconstructor_set-0-type_player': ['1'], 'serverrecordingrepeatconstructor_set-0-quantity': ['1'], 'serverrecordingrepeatconstructor_set-0-id': ['9'], 'serverrecordingrepeatconstructor_set-0-constructor': ['56'], 'serverrecordingrepeatconstructor_set-__prefix__-type': [''], 'serverrecordingrepeatconstructor_set-__prefix__-type_player': [''], 'serverrecordingrepeatconstructor_set-__prefix__-quantity': ['0'], 'serverrecordingrepeatconstructor_set-__prefix__-id': [''], 'serverrecordingrepeatconstructor_set-__prefix__-constructor': ['56'], 'gfxptsconstructor_set-TOTAL_FORMS': ['1'], 'gfxptsconstructor_set-INITIAL_FORMS': ['1'], 'gfxptsconstructor_set-MIN_NUM_FORMS': ['0'], 'gfxptsconstructor_set-MAX_NUM_FORMS': ['1000'], 'gfxptsconstructor_set-0-gfx': ['1'], 'gfxptsconstructor_set-0-license_type': ['2'], 'gfxptsconstructor_set-0-quantity': ['1'], 'gfxptsconstructor_set-0-id': ['20'], 'gfxptsconstructor_set-0-constructor': ['56'], 'gfxptsconstructor_set-__prefix__-gfx': [''], 'gfxptsconstructor_set-__prefix__-quantity': ['0'], 'gfxptsconstructor_set-__prefix__-id': [''], 'gfxptsconstructor_set-__prefix__-constructor': ['56'], 'microphone_quantity': ['5']}>


# {'csrfmiddlewaretoken': ['3KKKCltAbB4Gq2NCQvvI9I6RNPDmvsN8MUSYepBaflehyfPGneZ757X2iL1nY3wK'],
#  'name': ['ghjgfjhghjghj'],
#  'cameraptsconstructor_set-TOTAL_FORMS': ['1'],
#  'cameraptsconstructor_set-INITIAL_FORMS': ['0'],
#  'cameraptsconstructor_set-MIN_NUM_FORMS': ['0'],
#  'cameraptsconstructor_set-MAX_NUM_FORMS': ['1000'],
#  'cameraptsconstructor_set-0-cameras': ['2'],
#  'cameraptsconstructor_set-0-quantity': ['2'],
#  'cameraptsconstructor_set-0-id': [''],
#  'cameraptsconstructor_set-0-constructor': [''],
#  'cameraptsconstructor_set-__prefix__-cameras': [''],
#  'cameraptsconstructor_set-__prefix__-quantity': ['0'],
#  'cameraptsconstructor_set-__prefix__-id': [''],
#  'cameraptsconstructor_set-__prefix__-constructor': [''],
 
#  'opticptsconstructor_set-TOTAL_FORMS': ['0'], 'opticptsconstructor_set-INITIAL_FORMS': ['0'], 'opticptsconstructor_set-MIN_NUM_FORMS': ['0'], 'opticptsconstructor_set-MAX_NUM_FORMS': ['1000'], 'opticptsconstructor_set-__prefix__-optics': [''], 'opticptsconstructor_set-__prefix__-quantity': ['0'], 'opticptsconstructor_set-__prefix__-id': [''], 'opticptsconstructor_set-__prefix__-constructor': [''], 'serverrecordingrepeatconstructor_set-TOTAL_FORMS': ['0'], 'serverrecordingrepeatconstructor_set-INITIAL_FORMS': ['0'], 'serverrecordingrepeatconstructor_set-MIN_NUM_FORMS': ['0'], 'serverrecordingrepeatconstructor_set-MAX_NUM_FORMS': ['1000'], 'serverrecordingrepeatconstructor_set-__prefix__-type': [''], 'serverrecordingrepeatconstructor_set-__prefix__-type_player': [''], 'serverrecordingrepeatconstructor_set-__prefix__-quantity': ['0'], 'serverrecordingrepeatconstructor_set-__prefix__-id': [''], 'serverrecordingrepeatconstructor_set-__prefix__-constructor': [''], 'gfxptsconstructor_set-TOTAL_FORMS': ['0'], 'gfxptsconstructor_set-INITIAL_FORMS': ['0'], 'gfxptsconstructor_set-MIN_NUM_FORMS': ['0'], 'gfxptsconstructor_set-MAX_NUM_FORMS': ['1000'], 'gfxptsconstructor_set-__prefix__-gfx': [''], 'gfxptsconstructor_set-__prefix__-quantity': ['0'], 'gfxptsconstructor_set-__prefix__-id': [''], 'gfxptsconstructor_set-__prefix__-constructor': [''], 'microphone_quantity': ['2']}>