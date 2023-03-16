from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from place_broadcast.models import PlaceConstructor, PlaceCity, EventType


class AddBroadcastPlace(forms.ModelForm):
    """Form for PlaceConstructor model."""

    city_name = forms.ModelChoiceField(
        queryset=PlaceCity.objects.all(),
        label='Город',
        empty_label='Выберите город'
    )
    name = forms.CharField(
        label='Название Объекта',
        validators=[RegexValidator(
            '^[-()\".,!?a-zA-Z0-9_А-я\\s]*$',
            message='Только буквы и цифры'
        )],
        widget=forms.TextInput(
            attrs={'placeholder': 'Введите название объекта'}
        ),
    )
    address = forms.CharField(
        label='Адрес',
        widget=forms.TextInput(attrs={'placeholder': 'Адрес'})
    )
    contact_name = forms.CharField(
        label='ФИО ответственного лица на объекте',
        validators=[RegexValidator(
            '^[a-zA-ZА-я\\s]*$',
            message='Только буквы'
        )],
        widget=forms.TextInput(attrs={'placeholder': 'Введите ФИО'})
    )
    web = forms.URLField(
        label='Website Address',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'https://example.com'})
    )
    email_address = forms.EmailField(
        label='Email',
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': 'Введите адрес электронной почты'}
        )
    )
    phone = forms.CharField(
        label='Контактный телефон',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Номер телефона контактного лица',
            'data-mask': '(00) 000-00-00'
        }),
    )
    judge = forms.CharField(required=False,)
    judge_system = forms.CharField(
        label=False,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите информацию о судейской системе',
            'class': 'textinput form-control'
        }),
    )

    def __init__(self, *args, **kwargs):
        """Add city id and user to form,
        filters event types according to direction"""

        self.selected_city = kwargs.pop('city_id', None)
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['event_type'].queryset = EventType.objects.filter(
            direction=self.user.direction
        )
        if self.selected_city:
            self.fields['city_name'].initial = self.selected_city

    def clean(self):
        """Checks that three fields: name city, name, author,
        have unique constraint.
        Cleans field judge_system if 'judge' field is false"""

        city_name = self.cleaned_data.get('city_name')
        name = self.cleaned_data.get('name')
        dublicate = PlaceConstructor.objects.filter(
            city_name=city_name, name=name, author=self.user).count()
        if not self.instance.pk and dublicate > 0:
            raise ValidationError(
                f'Площадка с таким название уже существует в городе '
                f'{city_name}'
            )
        if not self.cleaned_data.get('judge'):
            self.cleaned_data['judge_system'] = ''
        return self.cleaned_data

    class Meta:
        model = PlaceConstructor
        exclude = ('author', )

        widgets = {
            'event_type': forms.CheckboxSelectMultiple()
        }
