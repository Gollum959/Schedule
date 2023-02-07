from django.forms import ModelForm
from place_broadcast.models import PlaceConstructor


class AddBroadcastPlace(ModelForm):

    class Meta:
        model = PlaceConstructor
        exclude = ('author', )
