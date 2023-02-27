from django.contrib import admin

from pts_requests.models import (PtsName, BroadCastType,
                                 PtsRequest, CommLineConstructor,
                                 TechCommLineConstructor, PlaceInsideBT,
                                 InternetLineConstructor)


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


@admin.register(PtsRequest)
class PtsRequestAdmin(admin.ModelAdmin):
    """Displaying the PtsRequest model in the admin panel."""

    list_display = ('name', 'broadcast_start_date', 'place', 'type',
                    'start_date', 'end_date', 'get_pts', 'pts_cfg', 'author')
    list_filter = ('author', 'broadcast_start_date', )
    search_fields = ('author', )
    inlines = (
        CommLineConstructors,
        TechCommLineConstructors,
        InternetLineConstructor
    )
