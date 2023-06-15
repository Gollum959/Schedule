from django.contrib import admin
from django.db.models import Q

from pts_config.models import PtsConstructor
from pts_requests.models import (PtsName, BroadCastType,
                                 PtsRequest, CommLineConstructor,
                                 TechCommLineConstructor, PlaceInsideBT,
                                 InternetLineConstructor,
                                 PtsRequestApprovalStages)


@admin.register(PtsName)
class PtsNameAdmin(admin.ModelAdmin):
    """Displaying the PtsName model in the admin panel."""
    list_display = ('name', 'head_fullname', 'head_contact',
                    'deputi_head_fullname', 'deputi_head_contact')


@admin.register(BroadCastType)
class BroadCastTypeAdmin(admin.ModelAdmin):
    """Displaying the BroadCastType model in the admin panel."""
    list_display = ('name', )


@admin.register(PlaceInsideBT)
class PlaceInsideBTAdmin(admin.ModelAdmin):
    """Displaying the PlaceInsideBT model in the admin panel."""
    list_display = ('name', )


@admin.register(CommLineConstructor)
class CommLineConstructorAdmin(admin.ModelAdmin):
    """Displaying the CommLineConstructor model in the admin panel."""
    fields = ('direction', 'custom', 'quantity', 'start', 'end')


class CommLineConstructors(admin.TabularInline):
    """Display communication lines in PTS request."""
    model = CommLineConstructor
    fields = ('direction', 'custom', 'quantity', 'start', 'end')
    extra = 1


@admin.register(TechCommLineConstructor)
class TechCommLineConstructorAdmin(admin.ModelAdmin):
    """Displaying the TechCommLineConstructor model in the admin panel."""
    fields = ('type', 'place', 'quantity', 'start', 'end')


class TechCommLineConstructors(admin.TabularInline):
    """Display tech communication lines in PTS request."""
    model = TechCommLineConstructor
    fields = ('type', 'place', 'quantity', 'start', 'end')
    extra = 1


@admin.register(InternetLineConstructor)
class InternetLineConstructorAdmin(admin.ModelAdmin):
    """Displaying the InternetLineConstructor model in the admin panel."""
    fields = ('speed', 'quantity', 'start', 'end')


class InternetLineConstructor(admin.TabularInline):
    """Display InternetLineConstructor lines in PTS request."""
    model = InternetLineConstructor
    fields = ('speed', 'quantity', 'start', 'end')
    extra = 1


@admin.register(PtsRequestApprovalStages)
class PtsRequestApprovalStagesAdmin(admin.ModelAdmin):
    """Displaying the PtsRequestApprovalStages model in the admin panel."""
    list_display = ('pts_request', 'steps', 'author',
                    'comment', 'create_date')


@admin.register(PtsRequest)
class PtsRequestAdmin(admin.ModelAdmin):
    """Displaying the PtsRequest model in the admin panel."""

    list_display = ('name', 'status', 'broadcast_start_date', 'place', 'type',
                    'start_date', 'end_date', 'pts_name', 'pts_cfg', 'author')
    list_filter = ('author', 'broadcast_start_date', )
    search_fields = ('author', )
    inlines = (
        CommLineConstructors,
        TechCommLineConstructors,
        InternetLineConstructor
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "pts_cfg":
            kwargs["queryset"] = PtsConstructor.objects.filter(
                Q(clone_conf=False) |
                Q(ptsrequest=request.resolver_match.kwargs.get('object_id'))
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
