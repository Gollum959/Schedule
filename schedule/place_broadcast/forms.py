from django.forms import ModelForm
from place_broadcast.models import PlaceConstructor


class AddBroadcastPlace(ModelForm):

    def __init__(self, *args, **kwargs):
        self.selected_city = kwargs.pop('city_id', None)
        super().__init__(*args, **kwargs)

        if self.selected_city:
            self.fields['city_name'].initial = self.selected_city

    class Meta:
        model = PlaceConstructor
        exclude = ('author', )
