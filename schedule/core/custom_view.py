from django.http import Http404
from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import PermissionDenied


class DetalInformationMixin:
    """Detail view for author or admin"""

    def get_object(self, queryset=None):
        """Check that only author can see detail information"""
        obj = super(DetalInformationMixin, self).get_object(queryset=queryset)
        if (
            obj.author != self.request.user
            and not self.request.user.is_admin
            and not self.request.user.is_moderator
        ):
            raise Http404()
        return obj


class UserToFormMixin:
    """Add user form kwargs"""

    def get_form_kwargs(self):
        kwargs = super(UserToFormMixin, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class EditOnlyAuthorMixin:
    """Edit only for for author"""

    def get_object(self, queryset=None):
        """Check that only author can see detail information"""
        obj = super(EditOnlyAuthorMixin, self).get_object(queryset=queryset)
        if obj.author != self.request.user:
            raise Http404()
        return obj


# class CreateOnlyMainDirectorMixin:
#     """Permision only for for main director or admin"""

#     def get_object(self, queryset=None):
#         """Check that only author can see detail information"""
#         obj = super(CreateOnlyMainDirectorMixin, self).get_object(
#             queryset=queryset
#         )
#         if self.request.user.is_main_director_or_admin:
#             raise Http404()
#         return obj


class CreateOnlyMainDirectorMixin(AccessMixin):
    """Permision only for for main director or admin"""

    def dispatch(self, request, *args, **kwargs):

        if (
            request.user.is_authenticated and
            self.request.user.is_main_director_or_admin
        ):
            return super().dispatch(request, *args, **kwargs)

        raise PermissionDenied('Permission denied')
