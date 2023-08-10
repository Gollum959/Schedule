from django.forms import (ModelForm,
                          ModelChoiceField,
                          inlineformset_factory,
                          DateTimeInput,
                          DateTimeField,)
from django.db.models import Q


from place_broadcast.models import PlaceConstructor, PlaceCity, EventType
from pts_requests.models import (PtsRequest,
                                 CommLineConstructor,
                                 TechCommLineConstructor,
                                 InternetLineConstructor)
from users.models import User
from pts_config.models import PtsConstructor


class AddRequestFrom(ModelForm):
    """Form for creating and updating PTS request."""

    city_name = ModelChoiceField(
        queryset=User.objects.none(),
        label='Город',
        empty_label='Выберите город'
    )
    director = ModelChoiceField(
        queryset=User.objects.all(),
        label='Режисер трасляции',
        empty_label='Выберете режиссера'
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
    broadcast_start_date = DateTimeField(
        widget=DateTimeInput(format='%Y-%m-%d %H:%M'),
        input_formats=['%Y-%m-%d %H:%M'],
        label='Дата и время начала трансляции')
    broadcast_end_date = DateTimeField(
        widget=DateTimeInput(format='%Y-%m-%d %H:%M'),
        input_formats=['%Y-%m-%d %H:%M'],
        label='Дата и время окончания трансляции')
    trakt_start_date = DateTimeField(
        widget=DateTimeInput(format='%Y-%m-%d %H:%M'),
        input_formats=['%Y-%m-%d %H:%M'],
        label='Дата и время начала тракта')
    trakt_end_date = DateTimeField(
        widget=DateTimeInput(format='%Y-%m-%d %H:%M'),
        input_formats=['%Y-%m-%d %H:%M'],
        label='Дата и время окончания тракта')

    def __init__(self, *args, **kwargs):
        """Method allows creating a link between
         the place and the configuration"""

        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['director'].queryset = User.objects.filter(
            direction=self.user.direction)
        self.fields['director'].initial = self.user
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
            'broadcast_end_date', 'trakt_start_date', 'trakt_end_date',
            'place', 'type', 'pts_cfg', 'director'
        ]


class TimeStartEnd(ModelForm):
    """Form for special widget DateTime."""
    start = DateTimeField(
        widget=DateTimeInput(format='%Y-%m-%d %H:%M'),
        input_formats=['%Y-%m-%d %H:%M'],
        label='Дата и время начала работ')
    end = DateTimeField(
        widget=DateTimeInput(format='%Y-%m-%d %H:%M'),
        input_formats=['%Y-%m-%d %H:%M'],
        label='Дата и время окончания работ')


class AddCommLine(TimeStartEnd):
    """Form for the communication line."""

    class Meta:
        model = CommLineConstructor
        fields = ['direction', 'custom', 'quantity', 'start', 'end', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['direction'].initial = 'from_pts'
        self.fields['quantity'].initial = 1


CommLineFormset = inlineformset_factory(
    PtsRequest, CommLineConstructor,
    form=AddCommLine,
    extra=0,
    can_delete=True
)


class AddTechCommLine(TimeStartEnd):
    """Form for the technical communication line."""

    class Meta:
        model = TechCommLineConstructor
        fields = ['type', 'place', 'quantity', 'start', 'end', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].initial = 'four'
        self.fields['place'].initial = 1
        self.fields['quantity'].initial = 1


TechCommLineFormset = inlineformset_factory(
    PtsRequest, TechCommLineConstructor,
    form=AddTechCommLine,
    extra=0,
    can_delete=True
)


class AddInternetLine(TimeStartEnd):
    """Form for the internet communication line."""

    class Meta:
        model = InternetLineConstructor
        fields = ['speed', 'phone', 'quantity', 'start', 'end', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['quantity'].initial = 1


InternetLineFormset = inlineformset_factory(
    PtsRequest, InternetLineConstructor,
    form=AddInternetLine,
    extra=0,
    can_delete=True
)

# Forms for time block


class UpdateTraktTime(ModelForm):
    """Form for moderating trakt time"""
    trakt_start_date = DateTimeField(
        widget=DateTimeInput(format='%Y-%m-%d %H:%M'),
        input_formats=['%Y-%m-%d %H:%M'])
    trakt_end_date = DateTimeField(
        widget=DateTimeInput(format='%Y-%m-%d %H:%M'),
        input_formats=['%Y-%m-%d %H:%M'])

    class Meta:
        model = PtsRequest
        fields = ['trakt_start_date', 'trakt_end_date', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['trakt_start_date'].required = True
        self.fields['trakt_end_date'].required = True


class UpdateTravelTime(ModelForm):
    """Form for moderating travel time"""
    start_date = DateTimeField(
        widget=DateTimeInput(format='%Y-%m-%d %H:%M'),
        input_formats=['%Y-%m-%d %H:%M'],
        label="Дата и время выезда ПТС с базы")
    end_date = DateTimeField(
        widget=DateTimeInput(format='%Y-%m-%d %H:%M'),
        input_formats=['%Y-%m-%d %H:%M'],
        label="Дата и время отьезда ПТС с объекта")
    start_date_arrival = DateTimeField(
        widget=DateTimeInput(format='%Y-%m-%d %H:%M'),
        input_formats=['%Y-%m-%d %H:%M'],
        label="Дата и время прибытия ПТС на объект")
    end_date_arrival = DateTimeField(
        widget=DateTimeInput(format='%Y-%m-%d %H:%M'),
        input_formats=['%Y-%m-%d %H:%M'],
        label="Дата и время прибытия ПТС на базу")

    class Meta:
        model = PtsRequest
        fields = ['start_date', 'start_date_arrival',
                  'end_date', 'end_date_arrival']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_date'].required = True
        self.fields['end_date'].required = True
        self.fields['start_date_arrival'].required = True
        self.fields['end_date_arrival'].required = True

# Forms for config block


class UpdatePTS(ModelForm):
    """Form for moderating type PTS"""

    class Meta:
        model = PtsRequest
        fields = ['pts_name', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pts_name'].required = True
