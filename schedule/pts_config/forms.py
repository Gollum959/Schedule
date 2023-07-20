import os
from django.db.models import Q
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

from pts_config.models import (PtsConstructor,
                               CameraPtsConstructor,
                               CameraBrend,
                               CameraModelBrend,
                               OpticBrend,
                               OpticModelBrend,
                               OpticPtsConstructor,
                               ServerRecordingRepeatConstructor,
                               ServerPlayerType,
                               ServerRecordingRepeatBrend,
                               ServerRecordingRepeatModelBrend,
                               GfxPtsConstructor,
                               MicrophonePtsConstructor,
                               MicrophoneBrend,
                               MicrophoneModelBrend,
                               Optic)
from pts_requests.models import PtsRequest


class CreatePtsConfigurationMixin(forms.ModelForm):
    """Mixin to creat configuration with 2 fields(image, name)
     and clean_image method"""

    image = forms.FileField()
    name = forms.CharField(
        label='Название конфигурации ПТС',
        validators=[RegexValidator(
            '^[-()«»\".,!?a-zA-Z0-9_А-я\\s]*$',
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
        self.fields['commentator_position'].label = 'Организовать комментаторскую позицию'
        self.fields['commentator_headsets'].label = 'Предоставить 2 гарнитуры'

        if self.place_id:
            self.fields['place'].initial = self.place_id

        self.fields['event_type'].label = 'Вид события'
        self.fields['event_type'].disabled = True
        if self.event_id:
            self.fields['event_type'].initial = self.event_id

    class Meta:
        model = PtsConstructor
        fields = ('place', 'event_type',
                  'name', 'microphone_quantity', 'microphone_comment', 'image',
                  'commentator_position', 'commentator_headsets',
                  'commentator_comment')
        widgets = {
            'microphone_comment': forms.Textarea(attrs={'rows': 5}),
            'commentator_comment': forms.Textarea(attrs={'rows': 4}),
        }


class AddPtsConfigOnBaseFrom(CreatePtsConfigurationMixin):
    """Form for creation user own configuration based on the basic
     configuration."""

    def __init__(self, *args, **kwargs):
        """Add user to form."""

        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False
        self.fields['commentator_position'].label = 'Организовать комментаторскую позицию'
        self.fields['commentator_headsets'].label = 'Предоставить 2 гарнитуры'

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
        fields = ('name', 'microphone_quantity', 'microphone_comment', 'image',
                  'commentator_position', 'commentator_headsets',
                  'commentator_comment')
        widgets = {
            'microphone_comment': forms.Textarea(attrs={'rows': 5}),
            'commentator_comment': forms.Textarea(attrs={'rows': 4}),
        }


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
        self.fields['type_player'].queryset = ServerPlayerType.objects.none()
        if 'serverrecordingrepeatconstructor_set-0-type' in self.data:
            try:
                # if validation fails, the queryset will not work correctly
                self.fields['type_player'].queryset = ServerPlayerType.\
                    objects.filter(visible_to_user=True).order_by('name')
            except (ValueError, TypeError):
                pass

        elif self.instance.pk:
            self.fields['type_player'].queryset = ServerPlayerType.objects.\
                filter(rec_rep_type=self.instance.type,
                       visible_to_user=True).order_by('name')

    class Meta:
        model = ServerRecordingRepeatConstructor
        fields = ['type', 'type_player', ]


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

# 4 modules for moderate cfg in request detail


class ModerateCamera(forms.ModelForm):
    """Form for moderate CameraPtsConstructor model."""

    quantity = forms.IntegerField(min_value=0, max_value=30, required=False)

    def __init__(self, *args, **kwargs):
        """Method allows creating a matrix of equipment"""

        super().__init__(*args, **kwargs)
        self.fields['cameras'].disabled = True
        self.fields['cameras'].widget.attrs['readonly'] = True
        pts_request = PtsRequest.objects.get(pts_cfg=self.instance.constructor)
        brend = CameraBrend.objects.filter(
            Q(type_pts=pts_request.pts_name.type) | Q(type_pts__isnull=True)
            ).filter(cameramodelbrend__type=self.instance.cameras).distinct()
        self.fields['brend'].queryset = brend
        self.fields['model'].queryset = CameraModelBrend.objects.none()

        if 'cameraptsconstructor_set-0-brend' in self.data:
            try:
                # if some validation appears, will be needed to change queryset
                self.fields['model'].queryset = CameraModelBrend.objects.all()\
                    .order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.model:
            self.fields['model'].queryset = CameraModelBrend.objects.filter(
                    brend=self.instance.brend_id, type=self.instance.cameras
                ).order_by('name')
        else:
            model = CameraModelBrend.objects.filter(
                brend=brend.first(), type=self.instance.cameras)
            self.initial['brend'] = brend.first()
            self.fields['model'].queryset = model
            self.initial['model'] = model.first()

    class Meta:
        model = CameraPtsConstructor
        fields = ['cameras', 'quantity', 'brend', 'model']

        widgets = {
            'cameras': forms.Select(
                attrs={'style': 'width:140px; height:30px'}),
        }


CameraModerateFormset = forms.inlineformset_factory(
    PtsConstructor, CameraPtsConstructor,
    form=ModerateCamera,
    extra=0,
    can_delete=True
)


class ModerateOptic(forms.ModelForm):
    """Form for moderate OpticPtsConstructor model."""

    quantity = forms.IntegerField(min_value=0, max_value=30, required=False)
    user_magnification = forms.ModelChoiceField(
        queryset=Optic.objects.all(),
    )

    def __init__(self, *args, **kwargs):
        """Method allows creating a matrix of equipment"""

        super().__init__(*args, **kwargs)
        self.fields['user_magnification'].initial = self.instance.optics
        self.__make_disable_readonly('user_magnification')
        pts_request = PtsRequest.objects.get(pts_cfg=self.instance.constructor)
        self.fields['optics'].queryset = Optic.objects.filter(
                opticmodelbrend__type__isnull=False
            ).filter(
                Q(
                    opticmodelbrend__brend__type_pts=pts_request.pts_name.type
                ) | Q(
                    opticmodelbrend__brend__type_pts__isnull=True
                )
            ).distinct().order_by('name')
        self.fields['brend'].queryset = OpticBrend.objects.none()
        self.fields['model'].queryset = OpticModelBrend.objects.none()

        if 'opticptsconstructor_set-0-brend' in self.data:
            try:
                # if some validation appears, will be needed to change queryset
                self.fields['brend'].queryset = OpticBrend.objects.all()
                self.fields['model'].queryset = OpticModelBrend.objects.all()
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['brend'].queryset = OpticBrend.objects.filter(
                    Q(
                        type_pts=pts_request.pts_name.type
                    ) | Q(type_pts__isnull=True)
                ).order_by('name')
            self.fields['model'].queryset = OpticModelBrend.objects.filter(
                    brend=self.instance.brend_id, type=self.instance.optics
                ).order_by('name')

    def __make_disable_readonly(self, field_name):
        self.fields[field_name].disabled = True
        self.fields[field_name].widget.attrs['readonly'] = True

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
    """Form for moderate ServerRecordingRepeatConstructor model."""

    quantity = forms.IntegerField(min_value=0, max_value=5, required=False)
    user_type_player = forms.ModelChoiceField(
        queryset=ServerPlayerType.objects.all(), required=False
    )

    def __init__(self, *args, **kwargs):
        """Method allows creating a matrix of equipment.
        Allows add new line in inlineformset_factory."""

        self.pts_request_id = kwargs.pop('request_pk', None)
        super().__init__(*args, **kwargs)
        pts_request = PtsRequest.objects.get(pk=self.pts_request_id)
        self.fields['brend'].queryset = ServerRecordingRepeatBrend.objects.\
            filter(type_pts=pts_request.pts_name.type)
        if hasattr(self.instance, 'type_player'):
            self.fields['user_type_player'].initial = self.instance.type_player
            self.__make_disable_readonly('type')

        self.__make_disable_readonly('user_type_player')
        self.fields['type_player'].queryset = ServerPlayerType.objects.filter(
            visible_to_user=False)
        self.fields['model'].queryset = ServerRecordingRepeatModelBrend.\
            objects.none()

        if 'serverrecordingrepeatconstructor_set-0-model' in self.data:
            try:
                # if some validation appears, will be needed to change queryset
                self.fields['model'].queryset =\
                    ServerRecordingRepeatModelBrend.objects.all().order_by(
                        'name'
                    )
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.model:
            self.fields['model'].queryset = ServerRecordingRepeatModelBrend.\
                objects.filter(brend=self.instance.brend_id).order_by('name')

    def __make_disable_readonly(self, field_name):
        """Makes fields disable and readonly."""
        self.fields[field_name].disabled = True
        self.fields[field_name].widget.attrs['readonly'] = True

    class Meta:
        model = ServerRecordingRepeatConstructor
        fields = ['type', 'user_type_player', 'type_player',
                  'quantity', 'brend', 'model']
        widgets = {
            'type': forms.Select(attrs={'style': 'width:160px; height:30px'}),
            'type_player': forms.Select(
                attrs={'style': 'width:160px; height:30px'}),
            'quantity': forms.TextInput(attrs={'style': 'width:80px'})
        }


ServerModerateFormset = forms.inlineformset_factory(
    PtsConstructor, ServerRecordingRepeatConstructor,
    form=ModerateServer,
    extra=2,
    can_delete=True
)


class ModerateMicrophones(forms.ModelForm):
    """Form for moderate MicrophonePtsConstructor model."""

    quantity = forms.IntegerField(min_value=0, max_value=15, required=False)

    def __init__(self, *args, **kwargs):
        """Method allows creating a matrix of equipment."""

        self.pts_request_id = kwargs.pop('request_pk', None)

        super().__init__(*args, **kwargs)
        pts_request = PtsRequest.objects.get(pk=self.pts_request_id)

        if self.instance.constructor_id:
            self.fields['brend'].queryset = MicrophoneBrend.objects.filter(
                    microphonemodelbrend__type_pts=pts_request.pts_name.type,
                    microphonemodelbrend__type_micro=self.instance.type
                ).distinct()
        else:
            self.fields['brend'].queryset = MicrophoneBrend.objects.filter(
                    microphonemodelbrend__type_pts=pts_request.pts_name.type,
                ).distinct()

        self.fields['model'].queryset = MicrophoneModelBrend.objects.none()

        if 'microphoneptsconstructor_set-0-brend' in self.data:
            try:
                # if some validation appears, will be needed to change queryset
                self.fields['model'].queryset = MicrophoneModelBrend.\
                    objects.all().order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['model'].queryset = MicrophoneModelBrend.\
                objects.filter(
                    brend=self.instance.brend_id,
                    type_micro=self.instance.type,
                    type_pts=pts_request.pts_name.type
                ).order_by('name')

    class Meta:
        model = MicrophonePtsConstructor
        fields = ['type', 'brend',
                  'model', 'quantity']
        widgets = {
            'quantity': forms.TextInput(attrs={'style': 'width:80px'})
        }


MicrophonesModerateFormset = forms.inlineformset_factory(
    PtsConstructor, MicrophonePtsConstructor,
    form=ModerateMicrophones,
    extra=5,
    can_delete=True
)


MicrophonesUpdateFormset = forms.inlineformset_factory(
    PtsConstructor, MicrophonePtsConstructor,
    form=ModerateMicrophones,
    extra=0,
    can_delete=True
)

# At this moment moderation of GFX is not nedeed

# class ModerateGfx(forms.ModelForm):

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['gfx'].disabled = True
#         self.fields['license_type'].disabled = True
#         self.fields['gfx'].required = False
#         self.fields['quantity'].disabled = True

#     class Meta:
#         model = GfxPtsConstructor
#         fields = ['gfx', 'judicial_system',
#                   'license_type', 'quantity']
#         widgets = {
#             'gfx': forms.Select(attrs={'style': 'width:160px; height:30px'}),
#             'quantity': forms.TextInput(attrs={'style': 'width:80px'})
#         }


# GfxModerateFormset = forms.inlineformset_factory(
#     PtsConstructor, GfxPtsConstructor,
#     form=ModerateGfx,
#     extra=0,
#     can_delete=True
# )
