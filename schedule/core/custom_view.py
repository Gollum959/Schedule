from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.http import Http404


class DetailViewOnlyAuthor(LoginRequiredMixin, DetailView):
    """Detail view for author or admin"""

    def get_object(self, queryset=None):
        """Check that only author can see detail information"""
        obj = super(DetailViewOnlyAuthor, self).get_object(queryset=queryset)
        if (
            obj.author != self.request.user
            and not self.request.user.is_admin
            and not self.request.user.is_moderator
        ):
            raise Http404()
        return obj
