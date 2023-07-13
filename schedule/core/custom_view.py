from django.http import Http404
from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import PermissionDenied


class DetalInformationMixin:
    """Detail view for author or admin"""

    def get_object(self, queryset=None):
        """Check that only author can see detail information"""
        obj = super().get_object(queryset=queryset)
        if (
            (self.request.user.is_admin or
                obj.author.direction == self.request.user.direction) or
            (
                obj.status in ('soundman', 'approved', 'approval') and
                self.request.user.is_soundman
            ) or
            (
                obj.status not in ('dtov', 'draft') and
                self.request.user.is_gdpt
            ) or
            (obj.status != 'draft' and self.request.user.is_dtov_headmaster) or
            (obj.status != 'draft' and self.request.user.is_moderator)
        ):
            return obj

        raise Http404()


class UserToFormMixin:
    """Add user form kwargs"""

    def get_form_kwargs(self):
        kwargs = super(UserToFormMixin, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class EditOnlyAuthorMixin:
    """Edit only for for author"""

    def get_object(self, queryset=None):
        """Checks that only author can see detail information"""
        obj = super(EditOnlyAuthorMixin, self).get_object(queryset=queryset)
        if obj.author != self.request.user:
            raise Http404()
        return obj


class EditOnlyAdminOrModeratorMixin:
    """Edit only for for author"""

    def get_object(self, queryset=None):
        """Checks that only author can see detail information"""
        obj = super(EditOnlyAdminOrModeratorMixin, self).get_object(
            queryset=queryset)
        if not self.request.user.is_admin_or_moderator:
            raise Http404()
        return obj


class EditOnlyAuthorAdminMainDirMixin:
    """Edit only for for author, admin or main director of author direction"""

    def get_object(self, queryset=None):
        """Check that only author and others can see detail information"""
        obj = super(EditOnlyAuthorAdminMainDirMixin, self).get_object(
            queryset=queryset)
        if (obj.author == self.request.user or
            self.request.user.is_admin or
            (self.request.user.is_main_director and
                obj.author.direction == self.request.user.direction)):
            return obj
        raise Http404()

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
