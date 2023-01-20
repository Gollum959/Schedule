from django.forms import ModelForm, ModelChoiceField

from pts_requests.models import PtsRequest
from place_broadcast.models import PlaceConstructor
from pts_config.models import PtsConstructor


class AddRequestFrom(ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['place'] = ModelChoiceField(
            queryset=PlaceConstructor.objects.filter(author=self.user),
            empty_label="(Nothing)"
        )
        self.fields['pts_cfg'] = ModelChoiceField(
            queryset=PtsConstructor.objects.filter(author=self.user),
            empty_label="(Nothing)"
        )

    class Meta:
        model = PtsRequest
        fields = [
            'broadcast_start_date', 'place', 'type',
            'start_date', 'end_date', 'pts_cfg'
        ]
