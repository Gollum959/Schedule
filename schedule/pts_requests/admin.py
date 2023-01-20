from django.contrib import admin

from pts_requests.models import (PtsName, BroadCastType, PtsRequest,
                                 CommLineConstructor, TechCommLineConstructor)


@admin.register(PtsName)
class PtsNameAdmin(admin.ModelAdmin):
    """Displaying the PtsName model in the admin panel."""
    list_display = ('name', 'head_fullname', 'head_contact',
                    'deputi_head_fullname', 'deputi_head_contact')


@admin.register(BroadCastType)
class BroadCastTypeAdmin(admin.ModelAdmin):
    """Displaying the BroadCastTypeAdmin model in the admin panel."""
    list_display = ('name', )


class CommLineConstructor(admin.TabularInline):
    """Display microphone in PTS config."""

    model = CommLineConstructor
    fields = ('direction', 'internet', 'quantity')
    extra = 1


class TechCommLineConstructor(admin.TabularInline):
    """Display GFX in PTS config."""

    model = TechCommLineConstructor
    fields = ('direction', 'four_wire_comm', 'vpn')
    extra = 1


@admin.register(PtsRequest)
class PtsRequestAdmin(admin.ModelAdmin):
    """Displaying the PtsRequest model in the admin panel."""

    list_display = ('broadcast_start_date', 'place', 'type', 'start_date',
                    'end_date', 'get_pts', 'pts_cfg', 'author')
    fields = ('broadcast_start_date', 'broadcast_end_date', 'place', 'type',
              'start_date', 'end_date', 'pts_name', 'pts_cfg',
              'commentator_monitor', 'commentator_console',
              'commentator_headset', 'author')
    list_filter = ('author', 'broadcast_start_date', )
    search_fields = ('author', )
    inlines = (CommLineConstructor, TechCommLineConstructor)
