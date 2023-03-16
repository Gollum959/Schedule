from typing import Any, Dict
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.deletion import RestrictedError
from django.http import Http404, HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView

from place_broadcast.forms import AddBroadcastPlace
from place_broadcast.models import PlaceConstructor, PlaceCity
from core.custom_view import EditOnlyAuthorAdminMainDirMixin, DetalInformationMixin


class CityBroadcastCreate(LoginRequiredMixin, CreateView):
    """View class for creation a city."""

    login_url = reverse_lazy('users:login')
    model = PlaceCity
    fields = ('name', )
    template_name = 'place_broadcast/create_city.html'

    def form_valid(self, form):
        """After save, form closes the popup and
        pass the new object to the main window"""

        instance = form.save()
        return HttpResponse(
            f'<script>opener.closePopup(window, '
            f'"{instance.pk}", "{instance}", "#id_city_name");</script>'
        )


class CitiesBroadcastView(LoginRequiredMixin, ListView):
    """View class for cities."""

    login_url = reverse_lazy('users:login')
    model = PlaceCity
    template_name = 'place_broadcast/list_cities.html'

    def post(self, request, *args, **kwargs):
        """Handles the site removal.
        Only admin and main director have permission."""

        placecity_list = PlaceCity.objects.all()
        place_to_be_deleted = get_object_or_404(
            PlaceConstructor, pk=request.POST.get('place_pk')
        )
        deleted_place = place_to_be_deleted.name
        city = place_to_be_deleted.city_name.name
        if request.method == 'POST' and request.user.is_main_director_or_admin:
            try:
                place_to_be_deleted.delete()
                exept = False
            except RestrictedError:
                exept = True

            return render(request, self.template_name, {
                'place_city': city,
                'placecity_list': placecity_list,
                'deleted_place': deleted_place,
                'exept': exept})
        else:
            raise Http404()

    def get_context_data(self, **kwargs):
        """Add to context city name."""

        city = self.request.GET.get('city')
        if city:
            context = {'place_city': city}
            kwargs.update(context)
        return super().get_context_data(**kwargs)


class PlacesBroadcastView(LoginRequiredMixin, ListView):
    """Sites ListView class."""

    login_url = reverse_lazy('users:login')
    model = PlaceConstructor
    template_name = 'place_broadcast/list_places.html'

    def get_queryset(self):
        """Filters sites by city ID. The admin and the moderator see all sites,
        other users only sites created by their department"""

        requests = PlaceConstructor.objects.none()
        city_id = self.request.GET.get('city_id', None)
        if city_id:
            requests = PlaceConstructor.objects.filter(
                city_name=city_id,
            )
        if not self.request.user.is_admin_or_moderator:
            requests = requests.filter(
                author__direction=self.request.user.direction
            )

        return requests

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Add to context city id"""

        data = super().get_context_data(**kwargs)
        data['city_id'] = self.request.GET.get('city_id', None)

        return data


class PlacesBroadcastDetail(
    DetalInformationMixin, LoginRequiredMixin, DetailView
):
    """Place detail view"""
    login_url = reverse_lazy('users:login')
    model = PlaceConstructor
    template_name = 'place_broadcast/place_detail.html'


class PlacesBroadcastCreate(LoginRequiredMixin, CreateView):
    """Create new broadcast site"""

    login_url = reverse_lazy('users:login')
    form_class = AddBroadcastPlace
    template_name = 'place_broadcast/create_places.html'

    def dispatch(self, request, *args, **kwargs):
        """Checks only admin or main director can create a site"""

        if not request.user.is_main_director_or_admin:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        """Adds attributes(user, city id) to form's kwargs."""

        kwargs = super().get_form_kwargs()
        kwargs.update({'city_id': self.request.GET.get('city_id')})
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        """After save redirects to sites page."""

        form.instance.author = self.request.user
        place = form.save()
        return redirect(
            reverse('place:places') + f'?city={place.city_name.name}')


class PlacesBroadcastEdit(EditOnlyAuthorAdminMainDirMixin,
                          LoginRequiredMixin,
                          UpdateView):
    """Sites UpdateView class."""

    login_url = reverse_lazy('users:login')
    form_class = AddBroadcastPlace
    model = PlaceConstructor
    template_name = 'place_broadcast/create_places.html'

    def get_form_kwargs(self):
        """Adds attributes(user, city id) to form's kwargs."""

        kwargs = super().get_form_kwargs()
        kwargs.update({'city_id': self.request.GET.get('city_id')})
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        """After save redirects to sites page."""

        place = form.save()
        return redirect(
            reverse('place:places') + f'?city={place.city_name.name}')
