from django.forms import ModelForm, ModelChoiceField, inlineformset_factory

from place_broadcast.models import PlaceConstructor
from pts_requests.models import (PtsRequest,
                                 CommLineConstructor,
                                 TechCommLineConstructor)
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
            'name', 'broadcast_start_date', 'broadcast_end_date', 'place',
            'type', 'pts_cfg', 'commentator_monitor', 'commentator_console',
            'commentator_headset'
        ]


class ModerateRequestFrom(ModelForm):

    class Meta:
        model = PtsRequest
        fields = [
            'start_date', 'end_date', 'trakt_start_date',
            'trakt_end_date', 'pts_name', 'status', 'comment'
        ]


class AddCommLine(ModelForm):

    class Meta:
        model = CommLineConstructor
        fields = ['direction', 'custom', 'internet', 'quantity']


CommLineFormset = inlineformset_factory(
    PtsRequest, CommLineConstructor,
    form=AddCommLine,
    extra=0,
    can_delete=True
)


class AddTechCommLine(ModelForm):

    class Meta:
        model = TechCommLineConstructor
        fields = ['direction', 'custom', 'four_wire_comm', 'vpn']


TechCommLineFormset = inlineformset_factory(
    PtsRequest, TechCommLineConstructor,
    form=AddTechCommLine,
    extra=0,
    can_delete=True
)
