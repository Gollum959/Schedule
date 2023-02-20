from django.contrib import admin

from pts_requests.models import (PtsName, BroadCastType,
                                 PtsRequest, CommLineConstructor,
                                 TechCommLineConstructor)


@admin.register(PtsName)
class PtsNameAdmin(admin.ModelAdmin):
    """Displaying the PtsName model in the admin panel."""
    list_display = ('name', 'head_fullname', 'head_contact',
                    'deputi_head_fullname', 'deputi_head_contact')


@admin.register(BroadCastType)
class BroadCastTypeAdmin(admin.ModelAdmin):
    """Displaying the BroadCastType model in the admin panel."""
    list_display = ('name', )


@admin.register(CommLineConstructor)
class CommLineConstructorAdmin(admin.ModelAdmin):
    """Displaying the CommLineConstructor model in the admin panel."""
    fields = ('direction', 'custom', 'quantity')


class CommLineConstructors(admin.TabularInline):
    """Display communication lines in PTS request."""
    model = CommLineConstructor
    fields = ('direction', 'custom', 'quantity')
    extra = 1


@admin.register(TechCommLineConstructor)
class TechCommLineConstructorAdmin(admin.ModelAdmin):
    """Displaying the TechCommLineConstructor model in the admin panel."""
    fields = ('type', 'place', 'quantity')


class TechCommLineConstructors(admin.TabularInline):
    """Display tech communication lines in PTS request."""
    model = TechCommLineConstructor
    fields = ('type', 'place', 'quantity')
    extra = 1


@admin.register(PtsRequest)
class PtsRequestAdmin(admin.ModelAdmin):
    """Displaying the PtsRequest model in the admin panel."""

    list_display = ('name', 'broadcast_start_date', 'place', 'type',
                    'start_date', 'end_date', 'get_pts', 'pts_cfg', 'author')
    list_filter = ('author', 'broadcast_start_date', )
    search_fields = ('author', )
    inlines = (CommLineConstructors, TechCommLineConstructors)
