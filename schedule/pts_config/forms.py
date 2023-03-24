import os
from django.db.models import Q
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

from pts_config.models import (PtsConstructor,
                               CameraPtsConstructor,
                               CameraBrend,
                               CameraModelBrend,
                               OpticPtsConstructor,
                               ServerRecordingRepeatConstructor,
                               GfxPtsConstructor,
                               Optic)
from pts_requests.models import PtsRequest


class CreatePtsConfigurationMixin(forms.ModelForm):
    """Mixin to creat configuration with 2 fields(image, name)
     and mclean_image method"""

    image = forms.FileField()
    name = forms.CharField(
        label='Название конфигурации ПТС',
        validators=[RegexValidator(
            '^[-()\".,!?a-zA-Z0-9_А-я\\s]*$',
            message='Только буквы и цифры'
        )],
        widget=forms.TextInput(
            attrs={'placeholder': 'Введите имя конфигурации'}),
    )

    def clean_image(self):
        """Checks if a file is an image or a pdf"""

        uploaded_file = self.cleaned_data['image']
        try:
            im = forms.ImageField()
            im.to_python(uploaded_file)
        except forms.ValidationError:
            name, ext = os.path.splitext(uploaded_file.name)
            if ext not in ['.pdf', '.PDF']:
                raise forms.ValidationError(
                    "Only images and PDF files allowed")
        return uploaded_file


class AddPtsConfigFrom(CreatePtsConfigurationMixin):
    """Form for creating base PTS configurations."""

    def __init__(self, *args, **kwargs):
        """Extracts a place and event type from kwargs.
        Adds an initial value for a place and event type."""

        self.place_id = kwargs.pop('place', None)
        self.event_id = kwargs.pop('event', None)
        super().__init__(*args, **kwargs)

        self.fields['place'].label = 'Название объекта'
        self.fields['place'].disabled = True
        if self.place_id:
            self.fields['place'].initial = self.place_id

        self.fields['event_type'].label = 'Вид события'
        self.fields['event_type'].disabled = True
        if self.event_id:
            self.fields['event_type'].initial = self.event_id

    class Meta:
        model = PtsConstructor
        fields = ('place', 'event_type',
                  'name', 'microphone_quantity', 'image')


class AddPtsConfigOnBaseFrom(CreatePtsConfigurationMixin):
    """Form for creation user own configuration based on the basic
     configuration."""

    def __init__(self, *args, **kwargs):
        """Add user to form."""

        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False

    def clean(self):
        """Checks that three fields: clone_conf, name, author,
        have unique constraint."""

        name = self.cleaned_data.get('name')
        dublicate = PtsConstructor.objects.filter(
            clone_conf=False, name=name, author=self.user).count()
        if not self.instance.pk and dublicate > 0:
            raise ValidationError('Конфигурация с таким именем уже существует')

        return self.cleaned_data

    class Meta:
        model = PtsConstructor
        fields = ('name', 'microphone_quantity', 'image')


class AddCamera(forms.ModelForm):
    """Form for CameraPtsConstructor model.
     Uses for creation base or onbase configuration"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cameras'].empty_label = 'Выберете камеру'

    class Meta:
        model = CameraPtsConstructor
        fields = ['cameras', 'quantity']


CameraFormset = forms.inlineformset_factory(
    PtsConstructor, CameraPtsConstructor,
    form=AddCamera,
    extra=0,
    can_delete=True
)


class AddOptic(forms.ModelForm):
    """Form for OpticPtsConstructor model.
     Uses for creation base or onbase configuration"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['optics'].empty_label = 'Выберете кратность'
        self.fields['optics'].queryset = Optic.objects.filter(
            visible_to_user=True)

    class Meta:
        model = OpticPtsConstructor
        fields = ['optics', 'quantity']


OpticFormset = forms.inlineformset_factory(
    PtsConstructor, OpticPtsConstructor,
    form=AddOptic,
    extra=0,
    can_delete=True
)


class AddServer(forms.ModelForm):
    """Form for ServerRecordingRepeatConstructor model.
     Uses for creation base or onbase configuration"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].empty_label = 'Выберете сервер'
        self.fields['type_player'].empty_label = 'Выберете конфигурацию'
        self.fields['type'].label = 'Тип сервера'
        self.fields['type_player'].label = 'Конфигурация'

    class Meta:
        model = ServerRecordingRepeatConstructor
        fields = ['type', 'type_player', 'quantity']


ServerFormset = forms.inlineformset_factory(
    PtsConstructor, ServerRecordingRepeatConstructor,
    form=AddServer,
    extra=0,
    can_delete=True
)


class AddGfx(forms.ModelForm):
    """Form for GfxPtsConstructor model.
     Uses for creation base or onbase configuration"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['gfx'].empty_label = 'Выберете сервер графики'
        self.fields['gfx'].label = 'Сервер графики'
        self.fields['license_type'].label = 'Тип лицензии'

    class Meta:
        model = GfxPtsConstructor
        fields = ['gfx', 'judicial_system',
                  'license_type', 'quantity']


GfxFormset = forms.inlineformset_factory(
    PtsConstructor, GfxPtsConstructor,
    form=AddGfx,
    extra=0,
    can_delete=True
)

# Try to create 4 module for cfg in request detail


class ModerateCamera(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cameras'].disabled = True
        self.fields['quantity'].disabled = True
        self.fields['cameras'].widget.attrs['readonly'] = True
        self.fields['quantity'].widget.attrs['readonly'] = True
        pts_request = PtsRequest.objects.get(pts_cfg=self.instance.constructor)
        self.fields['brend'].queryset = CameraBrend.objects.filter(
            Q(type_pts=pts_request.pts_name.type) | Q(type_pts__isnull=True)
            ).filter(cameramodelbrend__type=self.instance.cameras).distinct()
        self.fields['model'].queryset = CameraModelBrend.objects.none()

        if 'cameraptsconstructor_set-0-brend' in self.data:
            try:
                self.fields['model'].queryset = CameraModelBrend.objects.all()\
                    .order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['model'].queryset = CameraModelBrend.objects.filter(
                    brend=self.instance.brend_id, type=self.instance.cameras
                ).order_by('name')

    class Meta:
        model = CameraPtsConstructor
        fields = ['cameras', 'quantity', 'brend', 'model']

        widgets = {
            'cameras': forms.Select(
                attrs={'style': 'width:140px; height:30px'}),
            'quantity': forms.TextInput(attrs={'style': 'width:80px'})
        }


CameraModerateFormset = forms.inlineformset_factory(
    PtsConstructor, CameraPtsConstructor,
    form=ModerateCamera,
    extra=0,
    can_delete=True
)


class ModerateOptic(forms.ModelForm):

    user_magnification = forms.ModelChoiceField(
        queryset=Optic.objects.all(),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_magnification'].initial = self.instance.optics
        self.fields['user_magnification'].disabled = True
        self.fields['quantity'].disabled = True
        self.fields['user_magnification'].widget.attrs['readonly'] = True
        self.fields['quantity'].widget.attrs['readonly'] = True

    class Meta:
        model = OpticPtsConstructor
        fields = ['user_magnification', 'optics', 'quantity', 'brend', 'model']

        widgets = {
            'user_magnification': forms.Select(
                attrs={'style': 'width:140px; height:30px'}),
            'quantity': forms.TextInput(attrs={'style': 'width:80px'})
        }


OpticModerateFormset = forms.inlineformset_factory(
    PtsConstructor, OpticPtsConstructor,
    form=ModerateOptic,
    extra=0,
    can_delete=True
)


class ModerateServer(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].disabled = True
        self.fields['type_player'].disabled = True
        self.fields['type'].required = False
        self.fields['type_player'].required = False
        self.fields['quantity'].disabled = True

    class Meta:
        model = ServerRecordingRepeatConstructor
        fields = ['type', 'type_player', 'quantity']
        widgets = {
            'type': forms.Select(attrs={'style': 'width:160px; height:30px'}),
            'type_player': forms.Select(
                attrs={'style': 'width:160px; height:30px'}),
            'quantity': forms.TextInput(attrs={'style': 'width:80px'})
        }


ServerModerateFormset = forms.inlineformset_factory(
    PtsConstructor, ServerRecordingRepeatConstructor,
    form=ModerateServer,
    extra=0,
    can_delete=True
)


class ModerateGfx(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['gfx'].disabled = True
        self.fields['license_type'].disabled = True
        self.fields['gfx'].required = False
        self.fields['quantity'].disabled = True

    class Meta:
        model = GfxPtsConstructor
        fields = ['gfx', 'judicial_system',
                  'license_type', 'quantity']
        widgets = {
            'gfx': forms.Select(attrs={'style': 'width:160px; height:30px'}),
            'quantity': forms.TextInput(attrs={'style': 'width:80px'})
        }


GfxModerateFormset = forms.inlineformset_factory(
    PtsConstructor, GfxPtsConstructor,
    form=ModerateGfx,
    extra=0,
    can_delete=True
)
