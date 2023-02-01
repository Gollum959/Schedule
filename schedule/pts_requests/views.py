from typing import Any, Dict
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.urls import reverse_lazy

from pts_requests.models import PtsRequest
from pts_requests.forms import AddRequestFrom, CommLineFormset, TechCommLineFormset
from core.custom_view import (DetalInformationMixin,
                              UserToFormMixin,
                              EditOnlyAuthorMixin)


class PtsRequestsView(LoginRequiredMixin, ListView):
    """Requets list view"""
    login_url = reverse_lazy('users:login')
    model = PtsRequest
    template_name = 'pts_requests/list_requests.html'

    def get_queryset(self):
        if self.request.user.is_admin or self.request.user.is_moderator:
            return PtsRequest.objects.all()
        return PtsRequest.objects.filter(author=self.request.user)


class PtsRequestDetail(DetalInformationMixin, LoginRequiredMixin, DetailView):
    """Request detail view"""
    login_url = reverse_lazy('users:login')
    model = PtsRequest
    template_name = 'pts_requests/request_detail.html'


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


class PtsRequestEdit(
    UserToFormMixin, EditOnlyAuthorMixin,
    LoginRequiredMixin, UpdateView
):
    login_url = reverse_lazy('users:login')
    form_class = AddRequestFrom
    model = PtsRequest
    template_name = 'pts_requests/create_requests.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        data = super().get_context_data(**kwargs)

        if self.request.POST:
            data['commline'] = CommLineFormset(self.request.POST, instance=self.object)
            data['techcommline'] = TechCommLineFormset(self.request.POST, instance=self.object)
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
