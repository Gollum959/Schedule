from django.forms import ModelForm, ModelChoiceField, inlineformset_factory
from django import forms

from place_broadcast.models import PlaceConstructor, PlaceCity, EventType
from pts_requests.models import (PtsRequest,
                                 CommLineConstructor,
                                 TechCommLineConstructor,
                                 InternetLineConstructor)
from pts_config.models import PtsConstructor


class AddRequestFrom(ModelForm):
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
                self.fields['place'].queryset = (
                    PlaceConstructor.objects.filter(
                        city_name=city_id
                    )
                )
                self.fields['event_type'].queryset = EventType.objects.filter(
                    placeconstructor__pk=place_id,
                    direction=self.user.direction
                )
                self.fields['pts_cfg'].queryset = PtsConstructor.objects.filter(
                    place=place_id,
                    event_type=event_id
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
                event_type=self.instance.event_type
            )

        # self.fields['event_type'].queryset = EventType.objects.filter(
        #     direction=self.user.direction
        # )

    # image = forms.FileField()

    # def clean_image(self):
    #     uploaded_file = self.cleaned_data['image']
    #     try:
    #         im = forms.ImageField()
    #         im.to_python(uploaded_file)
    #     except forms.ValidationError:
    #         name, ext = os.path.splitext(uploaded_file.name)
    #         if ext not in ['.pdf', '.PDF']:
    #             raise forms.ValidationError(
    #                 "Only images and PDF files allowed")
    #     return uploaded_file

    class Meta:
        model = PtsRequest
        fields = [
            'name', 'city_name', 'place', 'event_type', 'broadcast_start_date',
            'broadcast_end_date', 'place', 'type', 'pts_cfg',
        ]


class ModerateRequestFrom(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pts_name'].empty_label = 'Название ПТС'
        self.fields['status'].empty_label = 'Изменить статус заявки'

    class Meta:
        model = PtsRequest
        fields = [
            'start_date', 'end_date', 'trakt_start_date',
            'trakt_end_date', 'pts_name', 'status', 'comment'
        ]
        widgets = {
            'start_date': forms.DateTimeInput(
                attrs={'placeholder': 'Выберите дату и время'}
            ),
            'end_date': forms.DateTimeInput(
                attrs={'placeholder': 'Выберите дату и время'}
            ),
        }


class AddCommLine(ModelForm):

    class Meta:
        model = CommLineConstructor
        fields = ['direction', 'custom', 'quantity', 'start', 'end', ]


CommLineFormset = inlineformset_factory(
    PtsRequest, CommLineConstructor,
    form=AddCommLine,
    extra=0,
    can_delete=True
)


class AddTechCommLine(ModelForm):

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

    class Meta:
        model = InternetLineConstructor
        fields = ['speed', 'quantity', 'start', 'end', ]


InternetLineFormset = inlineformset_factory(
    PtsRequest, InternetLineConstructor,
    form=AddInternetLine,
    extra=0,
    can_delete=True
)
