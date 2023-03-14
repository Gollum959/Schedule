from typing import Any, Dict
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required


from place_broadcast.forms import AddBroadcastPlace
from place_broadcast.models import PlaceConstructor, PlaceCity
from core.custom_view import DetalInformationMixin, EditOnlyAuthorMixin, EditOnlyAuthorAdminMainDirMixin


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

    def get_context_data(self, **kwargs):
        context = {'city_id': self.request.GET.get('city_id', None)}
        kwargs.update(context)
        return super().get_context_data(**kwargs)

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
            requests = PlaceConstructor.objects.filter(
                city_name=city_id,
            )
        if not self.request.user.is_admin or not self.request.user.is_moderator:
            requests = requests.filter(
                author__direction=self.request.user.direction
            )

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

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_main_director_or_admin:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'city_id': self.request.GET.get('city_id')})
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PlacesBroadcastEdit(EditOnlyAuthorAdminMainDirMixin, LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('users:login')
    form_class = AddBroadcastPlace
    model = PlaceConstructor
    template_name = 'place_broadcast/create_places.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'city_id': self.request.GET.get('city_id')})
        kwargs.update({'user': self.request.user})
        return kwargs
    

@login_required
def place_delete(request, pk):
    print(id)
    place_to_be_deleted = get_object_or_404(PlaceConstructor, pk=pk)
    city = place_to_be_deleted.city_name
    if request.method == 'POST' and request.user.is_main_director_or_admin:
        place_to_be_deleted.delete()

    return redirect(reverse('place:places') + f'?city_id={city.name}')

    # def form_valid(self, form):
    #     form.instance.author = self.request.user
    #     return super().form_valid(form)
