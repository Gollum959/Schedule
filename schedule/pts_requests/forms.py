from django.forms import ModelForm, ModelChoiceField, inlineformset_factory

from place_broadcast.models import PlaceConstructor, PlaceCity
from pts_requests.models import (PtsRequest,
                                 CommLineConstructor,
                                 TechCommLineConstructor)
from pts_config.models import PtsConstructor


class AddRequestFrom(ModelForm):
    city_name = ModelChoiceField(
        queryset=PlaceCity.objects.all(),
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['city_name'].queryset = PlaceCity.objects.filter(
            author=self.user
        )
        self.fields['place'].queryset = PlaceConstructor.objects.none()
        if 'city_name' in self.data:
            try:
                city_id = int(self.data.get('city_name'))
                self.fields['place'].queryset = (
                    PlaceConstructor.objects.filter(
                        author=self.user,
                        city_name=city_id
                    )
                )
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            place = PlaceConstructor.objects.get(pk=self.instance.place_id)
            self.fields['city_name'].initial = place.city_name
            self.fields['place'].queryset = PlaceConstructor.objects.filter(
                author=self.user,
                city_name=place.city_name.pk
            )
        self.fields['pts_cfg'] = ModelChoiceField(
            queryset=PtsConstructor.objects.filter(author=self.user),
            empty_label="(Nothing)"
        )

    def validate(self, value):
        """Check if value consists only of valid emails."""
        super().validate(value)

    class Meta:
        model = PtsRequest
        fields = [
            'name', 'broadcast_start_date', 'broadcast_end_date', 'city_name',
            'place', 'type', 'pts_cfg', 'commentator_monitor',
            'commentator_console', 'commentator_headset'
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
