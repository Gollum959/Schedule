from django.forms import ModelForm
from place_broadcast.models import PlaceConstructor, PlaceCity


class AddBroadcastPlace(ModelForm):

    def __init__(self, *args, **kwargs):
        self.selected_city = kwargs.pop('cities', None)
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        self.fields['city_name'].queryset = PlaceCity.objects.filter(
            author=self.user
        )
        if self.selected_city:
            self.fields['city_name'].initial = self.selected_city

    class Meta:
        model = PlaceConstructor
        exclude = ('author', )
