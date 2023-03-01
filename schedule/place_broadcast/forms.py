from django import forms
from django.core.validators import RegexValidator

from place_broadcast.models import PlaceConstructor
from place_broadcast.models import EventType


class AddBroadcastPlace(forms.ModelForm):
    name = forms.CharField(
        label='Название Объекта',
        validators=[RegexValidator(
            '^[0-9a-zA-ZА-я\s]*$',
            message='Только буквы и цифры'
        )],
        widget=forms.TextInput(attrs={'placeholder': 'Введите название объекта'})
    )
    address = forms.CharField(
        label='Адрес',
        widget=forms.TextInput(attrs={'placeholder': 'Адрес'})
    )
    contact_name = forms.CharField(
        label='ФИО ответственного лица на объекте',
        validators=[RegexValidator(
            '^[a-zA-ZА-я\s]*$',
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

    def __init__(self, *args, **kwargs):
        self.selected_city = kwargs.pop('city_id', None)
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['event_type'].queryset = EventType.objects.filter(
            direction=self.user.direction
        )
        if self.selected_city:
            self.fields['city_name'].initial = self.selected_city

    class Meta:
        model = PlaceConstructor
        exclude = ('author', )

        widgets = {
            'event_type': forms.CheckboxSelectMultiple()
        }
