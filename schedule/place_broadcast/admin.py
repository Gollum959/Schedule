from django.contrib import admin

from place_broadcast.models import PlaceConstructor, PlaceCity, EventType


@admin.register(PlaceConstructor)
class PlaceConstructorTypeAdmin(admin.ModelAdmin):
    """Displaying the BroadCastTypeAdmin model in the admin panel."""

    list_display = ('name', 'city_name', 'address',
                    'contact_name', 'phone', 'author', )
    list_filter = ('city_name', 'author')
    search_fields = ('city_name', 'contact_name', )


@admin.register(PlaceCity)
class PlaceCityAdmin(admin.ModelAdmin):
    """Displaying the PlaceCity model in the admin panel."""

    list_display = ('name', )


@admin.register(EventType)
class EvenTypeAdmin(admin.ModelAdmin):
    """Displaying the EventType model in the admin panel."""

    list_display = ('name', 'direction')
