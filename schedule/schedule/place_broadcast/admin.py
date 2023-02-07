from django.contrib import admin

from place_broadcast.models import PlaceConstructor


@admin.register(PlaceConstructor)
class PlaceConstructorTypeAdmin(admin.ModelAdmin):
    """Displaying the BroadCastTypeAdmin model in the admin panel."""

    list_display = ('name', 'city', 'address',
                    'contact_name', 'phone', 'author')
    list_filter = ('city', 'author')
    search_fields = ('name', 'contact_name', )
