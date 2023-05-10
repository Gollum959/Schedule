from django.forms import ModelForm, ModelChoiceField, inlineformset_factory
from django.db.models import Q


from place_broadcast.models import PlaceConstructor, PlaceCity, EventType
from pts_requests.models import (PtsRequest,
                                 CommLineConstructor,
                                 TechCommLineConstructor,
                                 InternetLineConstructor)
from pts_config.models import PtsConstructor


class AddRequestFrom(ModelForm):
    """Form for creating and updating PTS request."""

    city_name = ModelChoiceField(
        queryset=PlaceCity.objects.all(),
        label='Город',
        empty_label='Выберите город'
    )
    event_type = ModelChoiceField(
        queryset=EventType.objects.all(),
        label='Вид события',
        empty_label='Вид события'
    )
    pts_cfg = ModelChoiceField(
        queryset=PlaceConstructor.objects.all(),
        label='Конфигурация ПТС',
        empty_label='Выберите конфигурацию ПТС'
    )

    def __init__(self, *args, **kwargs):
        """Method allows creating a link between
         the place and the configuration"""

        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        self.fields['place'].empty_label = 'Выберите площадку'
        self.fields['type'].empty_label = 'Выберите вид работ'
        self.fields['event_type'].empty_label = 'Выберите вид события'

        self.fields['city_name'].queryset = PlaceCity.objects.filter(
            placeconstructor__isnull=False, ).distinct()
        self.fields['place'].queryset = PlaceConstructor.objects.none()
        self.fields['pts_cfg'].queryset = PtsConstructor.objects.none()
        self.fields['event_type'].queryset = EventType.objects.none()
        if 'city_name' in self.data:
            try:
                city_id = int(self.data.get('city_name'))
                place_id = int(self.data.get('place'))
                event_id = int(self.data.get('event_type'))
                cfg_id = int(self.data.get('pts_cfg'))
                self.fields['place'].queryset = (
                    PlaceConstructor.objects.filter(
                        city_name=city_id
                    )
                )
                self.fields['event_type'].queryset = EventType.objects.filter(
                    placeconstructor__pk=place_id,
                    direction=self.user.direction
                )
                self.fields['pts_cfg'].queryset = PtsConstructor.objects.\
                    filter(place=place_id, event_type=event_id).filter(
                        Q(Q(clone_conf=False) | Q(pk=cfg_id))
                    )
            except (ValueError, TypeError):
                pass

        elif self.instance.pk:
            place = PlaceConstructor.objects.get(pk=self.instance.place_id)
            self.fields['city_name'].initial = place.city_name
            self.fields['place'].queryset = PlaceConstructor.objects.filter(
                city_name=place.city_name.pk
            )
            self.fields['event_type'].queryset = EventType.objects.filter(
                placeconstructor__pk=place.pk,
                direction=self.user.direction
            )
            self.fields['pts_cfg'].queryset = PtsConstructor.objects.filter(
                place=self.instance.place,
                event_type=self.instance.event_type).filter(
                    Q(Q(clone_conf=False) | Q(pk=self.instance.pts_cfg.pk))
                )

    class Meta:
        model = PtsRequest
        fields = [
            'name', 'city_name', 'place', 'event_type', 'broadcast_start_date',
            'broadcast_end_date', 'place', 'type', 'pts_cfg',
        ]


class AddCommLine(ModelForm):
    """Form for the communication line."""

    class Meta:
        model = CommLineConstructor
        fields = ['direction', 'custom', 'quantity', 'start', 'end', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['direction'].initial = 'from_pts'


CommLineFormset = inlineformset_factory(
    PtsRequest, CommLineConstructor,
    form=AddCommLine,
    extra=0,
    can_delete=True
)


class AddTechCommLine(ModelForm):
    """Form for the technical communication line."""

    class Meta:
        model = TechCommLineConstructor
        fields = ['type', 'place', 'quantity', 'start', 'end', ]


TechCommLineFormset = inlineformset_factory(
    PtsRequest, TechCommLineConstructor,
    form=AddTechCommLine,
    extra=0,
    can_delete=True
)


class AddInternetLine(ModelForm):
    """Form for the internet communication line."""

    class Meta:
        model = InternetLineConstructor
        fields = ['speed', 'phone', 'quantity', 'start', 'end', ]


InternetLineFormset = inlineformset_factory(
    PtsRequest, InternetLineConstructor,
    form=AddInternetLine,
    extra=0,
    can_delete=True
)

# Forms for time block


class UpdateTraktTime(ModelForm):
    """Form for moderating trakt time"""

    class Meta:
        model = PtsRequest
        fields = ['trakt_start_date', 'trakt_end_date', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['trakt_start_date'].required = True
        self.fields['trakt_end_date'].required = True


class UpdateTravelTime(ModelForm):
    """Form for moderating travel time"""

    class Meta:
        model = PtsRequest
        fields = ['start_date', 'end_date', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_date'].required = True
        self.fields['end_date'].required = True

# Forms for config block


class UpdatePTS(ModelForm):
    """Form for moderating type PTS"""

    class Meta:
        model = PtsRequest
        fields = ['pts_name', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pts_name'].required = True
