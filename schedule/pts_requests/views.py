from datetime import date, timedelta, datetime
import os
from django.http import HttpResponse
# import locale
from django.http import QueryDict, FileResponse
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from typing import Any, Dict
from django.http import HttpResponseRedirect
from docxtpl import DocxTemplate

from place_broadcast.models import PlaceConstructor, EventType
from pts_config.views import PtsConfigCreateOnBase
from pts_requests.models import PtsRequest, PtsRequestApprovalStages
from pts_config.models import PtsConstructor, MicrophoneType
from pts_requests.forms import (AddRequestFrom,
                                UpdateTraktTime,
                                UpdateTravelTime,
                                UpdatePTS,
                                CommLineFormset,
                                TechCommLineFormset,
                                InternetLineFormset)
from pts_config.forms import (CameraModerateFormset,
                              OpticModerateFormset,
                              ServerModerateFormset,
                              MicrophonesModerateFormset,
                              MicrophonesUpdateFormset)
from core.custom_view import (DetalInformationMixin,
                              UserToFormMixin,
                              EditOnlyAuthorMixin)
from pts_config.models import MicrophoneBrend
from schedule.settings import MEDIA_ROOT


class PtsRequestsView(LoginRequiredMixin, ListView):
    """Requets list view."""

    login_url = reverse_lazy('users:login')
    model = PtsRequest
    template_name = 'pts_requests/list_requests.html'

    def get_queryset(self):
        """Different requests for different data and
         different level permission."""

        # requests = PtsRequest.objects.all()
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
            requests = PtsRequest.objects.filter(
                broadcast_start_date__date=self.request.GET.get('date')
            )
        else:
            requests = PtsRequest.objects.filter(
                Q(
                    status__in=['approval',
                                'soundman',
                                'final',
                                'gdpt',
                                'dtov',
                                'rejected'],
                    broadcast_start_date__gte=start_week
                ) |
                Q(
                    status__in=['draft', 'approved', 'cancel'],
                    broadcast_start_date__range=(start_week, end_week)
                )
            )

        user = self.request.user

        if user.is_admin:
            return requests

        if (user.is_moderator or user.is_dtov_headmaster):
            return requests.exclude(status='draft')

        if user.is_soundman:
            return requests.filter(status__in=(
                'soundman', 'approved')
            )

        if user.is_gdpt:
            return requests.exclude(status__in=('dtov', 'draft'))

        # requests = requests.filter(
        #     author__direction=self.request.user.direction
        # ).exclude(~Q(author=self.request.user), status='cancel')

        if user.is_main_director or user.is_director:
            return requests.filter(
                Q(status='approved') | Q(author__direction=user.direction)
            ).exclude(Q(status='draft') & ~Q(author=user))

        # if user.is_director:
        #     return requests.filter(~Q(
        #         ~Q(author=self.request.user)
        #         & Q(Q(status='draft') | Q(status='rejected'))))


class PtsRequestDetail(DetalInformationMixin, LoginRequiredMixin, DetailView):
    """Request detail view."""

    login_url = reverse_lazy('users:login')
    model = PtsRequest
    template_name = 'pts_requests/request_detail.html'


class PtsRequestCreate(UserToFormMixin, LoginRequiredMixin, CreateView):
    """Create PTS request view class."""

    login_url = reverse_lazy('users:login')
    form_class = AddRequestFrom
    model = PtsRequest
    template_name = 'pts_requests/create_requests.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Adds to context PTS request lines."""

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
        """Validation and save request and all related lines."""

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
            step = PtsRequestApprovalStages(
                pts_request=self.object,
                steps=1,
                author=self.request.user
            )
            step.save()
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
    """Update PTS request view class."""

    login_url = reverse_lazy('users:login')
    form_class = AddRequestFrom
    model = PtsRequest
    template_name = 'pts_requests/create_requests.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Adds to context PTS request lines."""

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
        """Validation and save request and all related lines."""

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


class PtsRequestCreateCfg(PtsConfigCreateOnBase):

    template_name = 'pts_config/create_pts_cgf_short.html'

    def form_valid(self, form):

        context = self.get_context_data()
        if not form.cleaned_data.get('image'):
            form.instance.image = context.get('cfg_info').image
        form.instance.event_type = context.get('cfg_info').event_type
        form.instance.place = context.get('cfg_info').place
        form.instance.author = self.request.user
        form.instance.base_conf = self.BASE_CFG
        pts_cfg_forms = [context['camera'], context['optic'],
                         context['server'], context['gfx']]
        if all([inline_form.is_valid() for inline_form in pts_cfg_forms]):
            self.object = form.save()
            for cfg_form in pts_cfg_forms:
                cfg_form.instance = self.object
                cfg_form.save()
        else:
            return self.render_to_response(self.get_context_data(form=form))

        return HttpResponse(
            f'<script>opener.closeCfgCreatePopup(window, '
            f'"{self.object.pk}", "{self.object.name}", "#id_pts_cfg");'
            f'</script>'
        )
        # return HttpResponseRedirect(self.get_success_url())


@login_required
def remove_draft_pts_request(request, pk):
    """Remove draft PTS request, only author."""

    pts_request = get_object_or_404(PtsRequest, pk=pk)
    if pts_request.author != request.user and not pts_request.is_draft:
        raise Http404()
    pts_request.delete()
    return redirect('pts_requests:index')


@login_required
def download_letter(request, pk):
    pts_request = get_object_or_404(PtsRequest, pk=pk)
    # locale.setlocale(locale.LC_ALL, 'ru_RU')
    month_names = {
        1: ' января ',
        2: ' февраля ',
        3: ' марта ',
        4: ' апреля ',
        5: ' мая ',
        6: ' июня ',
        7: ' июля ',
        8: ' августа ',
        9: ' сентября ',
        10: ' октября ',
        11: ' ноября ',
        12: ' декабря ',
    }
    speeds = {
        '1': '20/20 Мбит/c',
        '2': '80/40 Мбит/c',
        '3': '200/200 Мбит/c',
    }
    doc_template_path = os.path.join(MEDIA_ROOT, 'letters', 'template.docx')
    doc = DocxTemplate(doc_template_path)
    start_date_time = pts_request.broadcast_start_date
    end_date_time = pts_request.broadcast_end_date
    # start_trakt_time = pts_request.trakt_start_date
    # end_trakt_time = pts_request.trakt_end_date
    start_date = start_date_time.strftime('%d %#m %Y')
    start_mounth = start_date_time.month
    start_date = start_date.replace(
        f' {start_mounth} ',
        month_names[start_mounth]
    )

    comm_line = pts_request.commlineconstructor_set.all()
    internet_lines = pts_request.internetlineconstructor_set.all()
    tech_comm_line = pts_request.techcommlineconstructor_set.all()
    city_phone = [line.phone for line in internet_lines].count(True)

    comm_start_times = [line.start for line in comm_line]
    comm_end_times = [line.end for line in comm_line]
    comm_start_datetime = min(comm_start_times)
    if comm_start_datetime:
        comm_start_date = comm_start_datetime.strftime('%d %#m %Y')
        start_mounth = comm_start_datetime.month
        comm_start_date = comm_start_date.replace(
            f' {start_mounth} ',
            month_names[start_mounth]
        )
        comm_start_time = comm_start_datetime.strftime('%H:%M')
        comm_end_time = max(comm_end_times).strftime('%H:%M')

    tech_start_times = [line.start for line in internet_lines]
    tech_start_times.extend([line.start for line in tech_comm_line])
    tech_end_times = [line.end for line in internet_lines]
    tech_end_times.extend([line.end for line in tech_comm_line])
    tech_start_datetime = min(tech_start_times)
    if tech_start_datetime:
        tech_start_date = tech_start_datetime.strftime('%d %#m %Y')
        start_mounth = tech_start_datetime.month
        tech_start_date = tech_start_date.replace(
            f' {start_mounth} ',
            month_names[start_mounth]
        )
        tech_start_time = tech_start_datetime.strftime('%H:%M')
        tech_end_time = max(tech_end_times).strftime('%H:%M')

    arrive_time = (
        tech_start_datetime - timedelta(minutes=30)).strftime('%H:%M')

    # tech_lines_start_date = ''
    # tech_lines_end_time = ''
    # if len(tech_comm_line) > 0:
    #     tech_lines_start_date = tech_comm_line[0].start.strftime('%d %#m %Y')
    #     start_mounth = tech_comm_line[0].start.month
    #     tech_lines_start_date = tech_lines_start_date.replace(
    #         f' {start_mounth} ',
    #         month_names[start_mounth]
    #     )
    #     tech_lines_start_time = tech_comm_line[0].start.strftime('%H:%M')
    #     tech_lines_end_time = tech_comm_line[0].end.strftime('%H:%M')

    context = {
        'name': pts_request.name,
        'request_date': start_date,
        'start_time': start_date_time.strftime('%H:%M'),
        'end_time': end_date_time.strftime('%H:%M'),
        'place_name': pts_request.place.name,
        'place_city': pts_request.place.city_name.name,
        'place_adress': pts_request.place.address,
        'comm_line': comm_line,
        # 'trakt_date': start_date,
        # 'trakt_start_time': start_trakt_time.strftime('%H:%M'),
        # 'trakt_end_time': end_trakt_time.strftime('%H:%M'),
        'tech_comm_line': tech_comm_line,
        'internet_comm_line': internet_lines,
        'city_phone': city_phone,
        'speeds': speeds,
        'comm_lines_start_date': comm_start_date,
        'comm_lines_start_time': comm_start_time,
        'comm_lines_end_time': comm_end_time,
        'tech_lines_start_date': tech_start_date,
        'tech_lines_start_time': tech_start_time,
        'tech_lines_end_date': tech_end_time,
        'arrive_time': arrive_time,
        'moderator_name': pts_request.moderator.get_fio,
        'moderator_job_title': pts_request.moderator.position,
        'moderator_phone': pts_request.moderator.phone_number,
        'pts_head_name': pts_request.pts_name.head_fullname,
        'pts_name': pts_request.pts_name,
        'pts_phone': pts_request.pts_name.head_contact,
        'director_name': pts_request.director.get_fio,
        'director_job_title': pts_request.director.position,
        'director_phone': pts_request.author.phone_number,
    }
    doc.render(context)
    letter_name = f'letterID-{pts_request.pk}.docx'
    letter_directory = os.path.join(
        os.path.join(MEDIA_ROOT, 'letters'),
        str(pts_request.broadcast_start_date.date())
    )
    letter_full_path = os.path.join(letter_directory, letter_name)
    os.makedirs(letter_directory, exist_ok=True)
    doc.save(letter_full_path)
    file_contents = open(letter_full_path, 'rb')
    response = FileResponse(file_contents)
    response['Content-Type'] = 'application/msword'
    response['Content-Disposition'] = f'attachment; filename={letter_name}'
    return response


@login_required
def load_places(request):
    """Loading places by city."""

    city_id = request.GET.get('city_name')
    if city_id:
        places = PlaceConstructor.objects.filter(
            city_name=city_id, ).order_by('name')
    else:
        places = PlaceConstructor.objects.none()
    return render(
        request,
        'pts_requests/place_dropdown_list_options.html',
        {'places': places}
    )


@login_required
def load_event_type(request):
    """Loading event type by place."""

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
    """Loading pts configuratins by place and event type."""

    event_id = request.GET.get('event_id')
    place_id = request.GET.get('place_id')
    if event_id:
        cfgs = PtsConstructor.objects.filter(
            place=place_id, event_type=event_id, clone_conf=False).filter(
            Q(author=request.user) | Q(base_conf=True)).order_by('name')
    else:
        cfgs = PtsConstructor.objects.none()
    modal_id = ("#NoBaseDirectorModal"
                if request.user.is_main_director_or_admin else "#NoBaseModal")
    return render(
        request,
        'pts_requests/cfg_dropdown_list_options.html',
        {'cfgs': cfgs, "modal_id": modal_id}
    )


@login_required
def load_cfg_detail(request):
    """Loading pts configuratin by id."""

    cfg_id = request.GET.get('id')
    cfg = get_object_or_404(PtsConstructor, pk=cfg_id) if cfg_id else None
    return render(
        request,
        'pts_requests/cfg_short_detail.html',
        {'cfg': cfg}
    )

# View functions for time block


@login_required
def time_trakt_edit_form(request, pk):
    """View function for moderating trakt time."""

    ptsrequest = get_object_or_404(PtsRequest, pk=pk)

    if request.GET.get('step') == 'back':
        return render(
            request,
            'includes/time_trakt.html',
            {'ptsrequest': ptsrequest}
        )

    # initial_dict = {}
    # if not ptsrequest.trakt_start_date:
    #     initial_dict['trakt_start_date'] = (
    #         ptsrequest.broadcast_start_date - timedelta(hours=1))
    # if not ptsrequest.trakt_end_date:
    #     initial_dict['trakt_end_date'] = (
    #         ptsrequest.broadcast_start_date - timedelta(minutes=10))

    if request.method == 'PUT':
        data = QueryDict(request.body).dict()
        form = UpdateTraktTime(data, instance=ptsrequest)
        context = {'ptsrequest': ptsrequest}
        if form.is_valid():
            form.instance.moderator = request.user
            form.save()
            return render(request, 'includes/time_trakt.html', context)

        context['form'] = form
        return render(request, 'includes/time_trakt_edit.html', context)

    # form = UpdateTraktTime(instance=ptsrequest, initial=initial_dict)
    form = UpdateTraktTime(instance=ptsrequest)
    context = {'ptsrequest': ptsrequest, 'form': form}
    return render(request, 'includes/time_trakt_edit.html', context)


@login_required
def time_travel_edit_form(request, pk):
    """View function for moderating travel time."""

    ptsrequest = get_object_or_404(PtsRequest, pk=pk)

    if request.GET.get('step') == 'back':
        return render(
            request,
            'includes/time_travel.html',
            {'ptsrequest': ptsrequest}
        )

    initial_dict = {}
    if not ptsrequest.start_date:
        work_start_date = ptsrequest.broadcast_start_date - timedelta(hours=12)
        initial_dict['start_date'] = work_start_date.strftime(
            '%Y-%m-%d %H:%M')
    if not ptsrequest.end_date:
        work_end_date = ptsrequest.broadcast_end_date + timedelta(hours=2)
        initial_dict['end_date'] = work_end_date.strftime(
            '%Y-%m-%d %H:%M')

    if request.method == 'PUT':
        data = QueryDict(request.body).dict()
        form = UpdateTravelTime(data, instance=ptsrequest)
        context = {'ptsrequest': ptsrequest}
        if form.is_valid():
            form.instance.moderator = request.user
            form.save()
            return render(request, 'includes/time_travel.html', context)

        context['form'] = form
        return render(request, 'includes/time_travel_edit.html', context)

    form = UpdateTravelTime(instance=ptsrequest, initial=initial_dict)
    context = {'ptsrequest': ptsrequest, 'form': form}
    return render(request, 'includes/time_travel_edit.html', context)

# View functions for config block


@login_required
def config_choice_pts_edit_form(request, pk):
    """View function for moderating type PTS."""

    ptsrequest = get_object_or_404(PtsRequest, pk=pk)

    if request.GET.get('step') == 'back':
        return render(
            request,
            'includes/config_choice_pts.html',
            {'ptsrequest': ptsrequest}
        )

    if request.method == 'PUT':
        data = QueryDict(request.body).dict()
        form = UpdatePTS(data, instance=ptsrequest)
        context = {'ptsrequest': ptsrequest}
        if form.is_valid():
            form.save()
            form.instance.moderator = request.user
            return render(request, 'includes/config_choice_pts.html',
                          context)

        context['form'] = form
        return render(request, 'includes/config_choice_pts_edit.html', context)

    form = UpdatePTS(instance=ptsrequest)
    context = {'ptsrequest': ptsrequest, 'form': form}
    return render(request, 'includes/config_choice_pts_edit.html', context)


@login_required
def config_cameras_edit_form(request, pk):
    """View function for moderation of block with cameras."""

    ptsrequest = get_object_or_404(PtsRequest, pk=pk)

    if not ptsrequest.pts_name:
        return render(
            request,
            'includes/config_cameras.html',
            {'ptsrequest': ptsrequest,
             'message': 'Выберете ПТС'}
        )

    if request.GET.get('step') == 'back':
        return render(
            request,
            'includes/config_cameras.html',
            {'ptsrequest': ptsrequest}
        )

    if request.method == 'POST':
        form = CameraModerateFormset(request.POST, instance=ptsrequest.pts_cfg)
        context = {'ptsrequest': ptsrequest}
        if form.is_valid():
            ptsrequest.moderator = request.user
            ptsrequest.save()
            form.save()
            return render(request, 'includes/config_cameras.html',
                          context)

        context['camera_forms'] = form
        return render(request, 'includes/config_cameras_edit.html', context)

    camera_forms = CameraModerateFormset(instance=ptsrequest.pts_cfg)
    context = {'ptsrequest': ptsrequest, 'camera_forms': camera_forms}
    return render(request, 'includes/config_cameras_edit.html', context)


@login_required
def config_optics_edit_form(request, pk):
    """View function for moderation of block with optics."""

    ptsrequest = get_object_or_404(PtsRequest, pk=pk)

    if not ptsrequest.pts_name:
        return render(
            request,
            'includes/config_optics.html',
            {'ptsrequest': ptsrequest,
             'message': 'Выберете ПТС'}
        )

    if request.GET.get('step') == 'back':
        return render(
            request,
            'includes/config_optics.html',
            {'ptsrequest': ptsrequest}
        )

    if request.method == 'POST':
        form = OpticModerateFormset(request.POST,
                                    instance=ptsrequest.pts_cfg,
                                    form_kwargs={'request_pk': pk})
        context = {'ptsrequest': ptsrequest}

        if form.is_valid():
            ptsrequest.moderator = request.user
            ptsrequest.save()
            form.save()
            return render(request, 'includes/config_optics.html',
                          context)

        context['optic_forms'] = form
        return render(request, 'includes/config_optics_edit.html', context)

    optic_forms = OpticModerateFormset(
        instance=ptsrequest.pts_cfg,
        form_kwargs={'request_pk': pk}
    )
    context = {'ptsrequest': ptsrequest, 'optic_forms': optic_forms}
    return render(request, 'includes/config_optics_edit.html', context)


@login_required
def config_servers_edit_form(request, pk):
    """View function for moderation of block with servers."""

    ptsrequest = get_object_or_404(PtsRequest, pk=pk)

    if not ptsrequest.pts_name:
        return render(
            request,
            'includes/config_servers.html',
            {'ptsrequest': ptsrequest,
             'message': 'Выберете ПТС'}
        )

    if request.GET.get('step') == 'back':
        return render(
            request,
            'includes/config_servers.html',
            {'ptsrequest': ptsrequest}
        )

    if request.method == 'POST':
        form = ServerModerateFormset(
            request.POST,
            instance=ptsrequest.pts_cfg,
            form_kwargs={'request_pk': pk}
        )
        context = {'ptsrequest': ptsrequest}
        if form.is_valid():
            ptsrequest.moderator = request.user
            ptsrequest.save()
            form.save()
            return render(request, 'includes/config_servers.html',
                          context)

        context['server_forms'] = form
        return render(request, 'includes/config_servers_edit.html', context)

    server_forms = ServerModerateFormset(
        instance=ptsrequest.pts_cfg,
        form_kwargs={'request_pk': pk}
    )
    context = {'ptsrequest': ptsrequest, 'server_forms': server_forms}
    return render(request, 'includes/config_servers_edit.html', context)


@login_required
def config_microphones_edit_form(request, pk):
    """View function for moderation of block with microphones."""

    ptsrequest = get_object_or_404(PtsRequest, pk=pk)

    if not ptsrequest.pts_name:
        return render(
            request,
            'includes/config_microphones.html',
            {'ptsrequest': ptsrequest,
             'message': 'Выберете ПТС'}
        )

    if request.GET.get('step') == 'back':
        return render(
            request,
            'includes/config_microphones.html',
            {'ptsrequest': ptsrequest}
        )

    if request.method == 'POST':
        form = MicrophonesModerateFormset(
            request.POST,
            instance=ptsrequest.pts_cfg,
            form_kwargs={'request_pk': pk}
        )
        context = {'ptsrequest': ptsrequest}
        if form.is_valid():
            ptsrequest.soundman = request.user
            ptsrequest.save()
            form.save()
            return render(request, 'includes/config_microphones.html',
                          context)

        context['microphones_forms'] = form
        return render(
            request,
            'includes/config_microphones_edit.html',
            context
        )

    if not ptsrequest.pts_cfg.microphoneptsconstructor_set.count():
        microphones_forms = MicrophonesModerateFormset(
            instance=ptsrequest.pts_cfg,
            form_kwargs={'request_pk': pk}
        )
        type_microphone = []
        for microphone in MicrophoneType.objects.all().order_by('name'):
            type_microphone.append({'type': microphone})
        for subform, data in zip(microphones_forms.forms, type_microphone):
            subform.fields.get('brend').queryset = MicrophoneBrend.objects.\
                filter(
                    microphonemodelbrend__type_pts=ptsrequest.pts_name.type,
                    microphonemodelbrend__type_micro=data.get('type')
                ).distinct()
            subform.initial = data
    else:
        microphones_forms = MicrophonesUpdateFormset(
            instance=ptsrequest.pts_cfg,
            form_kwargs={'request_pk': pk}
        )

    context = {
        'ptsrequest': ptsrequest,
        'microphones_forms': microphones_forms
    }
    return render(request, 'includes/config_microphones_edit.html', context)


# view functions to change request status

@login_required
def change_status_to_on_approval(request, pk):
    """Change PTS request status from draft to on approval."""

    pts_request = get_object_or_404(PtsRequest, pk=pk)
    if pts_request.author != request.user:
        raise Http404()
    step = PtsRequestApprovalStages(
                pts_request=pts_request,
                steps=3,
                author=request.user
            )
    step.save()
    # pts_request.trakt_start_date = (
    #     pts_request.broadcast_start_date - timedelta(hours=1)
    # )
    # pts_request.trakt_end_date = (
    #     pts_request.broadcast_start_date - timedelta(minutes=10)
    # )
    pts_request.status = 'approval'
    pts_request.save()
    return redirect('pts_requests:request_detail', pk=pts_request.pk)


@login_required
def change_status_to_reject(request, pk):
    """Change PTS request status to reject."""

    pts_request = get_object_or_404(PtsRequest, pk=pk)
    comment = request.POST.get('comment', '')
    step = request.POST.get('step')
    if (
        (
            not request.user.is_admin_or_moderator
            and pts_request.status != "soundman"
        ) or (
            not request.user.is_soundman_or_admin
            and pts_request.status == "soundman"
        )
    ):
        raise Http404()
    pts_request.status = step if step == 'soundman' else 'rejected'
    history_step = 2 if pts_request.status == 'rejected' else 4
    step = PtsRequestApprovalStages(
                pts_request=pts_request,
                steps=history_step,
                author=request.user,
                comment=comment
            )
    step.save()
    pts_request.save()
    return redirect('pts_requests:index')


@login_required
def change_status_to_cancel(request, pk):
    """Change PTS request status to cancel."""

    pts_request = get_object_or_404(PtsRequest, pk=pk)
    if request.user != pts_request.author:
        raise Http404()
    pts_request.status = 'cancel'
    pts_request.save()
    return redirect('pts_requests:index')


@login_required
def change_status_to_on_soundman(request, pk):
    """Change PTS request status from on approval to soundman."""

    pts_request = get_object_or_404(PtsRequest, pk=pk)
    if not request.user.is_admin_or_moderator:
        raise Http404()
    step = PtsRequestApprovalStages(
                pts_request=pts_request,
                steps=4,
                author=request.user,
            )
    step.save()
    pts_request.status = 'soundman'
    pts_request.save()
    return redirect('pts_requests:index')


@login_required
def change_status_to_final(request, pk):
    """Change PTS request status from on soundman to final."""

    pts_request = get_object_or_404(PtsRequest, pk=pk)
    if not request.user.is_soundman_or_admin:
        raise Http404()
    step = PtsRequestApprovalStages(
                pts_request=pts_request,
                steps=5,
                author=request.user,
            )
    step.save()
    pts_request.status = 'final'
    pts_request.save()
    return redirect('pts_requests:index')


@login_required
def change_status_to_gdpt(request, pk):
    """Change PTS request status from final to gdpt."""

    pts_request = get_object_or_404(PtsRequest, pk=pk)
    if not request.user.is_admin_or_moderator:
        raise Http404()
    step = PtsRequestApprovalStages(
                pts_request=pts_request,
                steps=6,
                author=request.user,
            )
    step.save()
    pts_request.status = 'gdpt'
    pts_request.moderator = request.user
    pts_request.save()
    return redirect('pts_requests:index')


@login_required
def change_status_to_dtov(request, pk):
    """Change PTS request status from gdpt to dtov."""

    pts_request = get_object_or_404(PtsRequest, pk=pk)
    if not request.user.is_gdpt_or_admin:
        raise Http404()
    step = PtsRequestApprovalStages(
                pts_request=pts_request,
                steps=7,
                author=request.user,
            )
    step.save()
    pts_request.status = 'dtov'
    pts_request.save()
    return redirect('pts_requests:index')


@login_required
def change_status_to_approved(request, pk):
    """Change PTS request status from gdpt to dtov."""

    pts_request = get_object_or_404(PtsRequest, pk=pk)
    if not request.user.is_dtov_headmaster_or_admin:
        raise Http404()
    step = PtsRequestApprovalStages(
                pts_request=pts_request,
                steps=8,
                author=request.user,
            )
    step.save()
    pts_request.status = 'approved'
    pts_request.save()
    return redirect('pts_requests:index')


# Validation hmx block

@login_required
def validate_on_aprovall_status(request, pk):
    pts_request = get_object_or_404(PtsRequest, pk=pk)
    result = True
    message_error = {
        'pts': False,
        'cam': False,
        'opt': False,
        'server': False,
    }
    if pts_request.pts_name is None:
        result = False
        message_error['pts'] = True
    if not pts_request.pts_cfg.cameraptsconstructor_set.filter(
        cameras__isnull=False,
        brend__isnull=False,
        model__isnull=False
    ).exists():
        result = False
        message_error['cam'] = True
    if not pts_request.pts_cfg.opticptsconstructor_set.filter(
        optics__isnull=False,
        brend__isnull=False,
        model__isnull=False
    ).exists():
        result = False
        message_error['opt'] = True
    if not pts_request.pts_cfg.serverrecordingrepeatconstructor_set.filter(
        type__isnull=False,
        type_player__isnull=False,
        brend__isnull=False,
        model__isnull=False
    ).exists():
        result = False
        message_error['server'] = True

    if result:
        return render(
            request,
            'includes/validations/approval_message.html',
            {'ptsrequest': pts_request}
        )

    return render(
            request,
            'includes/validations/error_message.html',
            {'message_error': message_error}
        )
