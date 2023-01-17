from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.http import Http404


from pts_requests.models import PtsRequest
from pts_requests.forms import AddRequestFrom
from core.custom_view import DetailViewOnlyAuthor


class PtsRequestsView(LoginRequiredMixin, ListView):
    """Requets list view"""
    login_url = reverse_lazy('users:login')
    model = PtsRequest
    template_name = 'pts_requests/list_requests.html'

    def get_queryset(self):
        if self.request.user.is_admin or self.request.user.is_moderator:
            return PtsRequest.objects.all()
        return PtsRequest.objects.filter(author=self.request.user)


class PtsRequestDetail(DetailViewOnlyAuthor):
    """Request detail view"""
    login_url = reverse_lazy('users:login')
    model = PtsRequest
    template_name = 'pts_requests/request_detail.html'


class PtsRequestCreate(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('users:login')
    form_class = AddRequestFrom
    model = PtsRequest
    template_name = 'pts_requests/create_requests.html'

    def get_form_kwargs(self):
        kwargs = super(PtsRequestCreate, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PtsRequestEdit(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('users:login')
    form_class = AddRequestFrom
    model = PtsRequest
    template_name = 'pts_requests/create_requests.html'

    def get_form_kwargs(self):
        kwargs = super(PtsRequestEdit, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_object(self, queryset=None):
        """Check that only author can see detail information"""
        obj = super(PtsRequestEdit, self).get_object(queryset=queryset)
        if (
            obj.author != self.request.user
            and not self.request.user.is_admin
            and not self.request.user.is_moderator
        ):
            raise Http404()
        return obj
