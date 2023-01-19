from django.contrib import admin

from pts_requests.models import PtsName, BroadCastType, PtsRequest


@admin.register(PtsName)
class PtsNameAdmin(admin.ModelAdmin):
    """Displaying the PtsName model in the admin panel."""
    list_display = ('name', 'head_fullname', 'head_contact',
                    'deputi_head_fullname', 'deputi_head_contact')


@admin.register(BroadCastType)
class BroadCastTypeAdmin(admin.ModelAdmin):
    """Displaying the BroadCastTypeAdmin model in the admin panel."""
    list_display = ('name', )


@admin.register(PtsRequest)
class PtsRequestAdmin(admin.ModelAdmin):
    """Displaying the PtsRequest model in the admin panel."""

    list_display = ('broadcast_date', 'place', 'type', 'start_date',
                    'end_date', 'pts_name', 'pts_cfg', 'author')
    list_filter = ('author', 'broadcast_date', )
    search_fields = ('author', )
    list_editable = ('pts_name', )
