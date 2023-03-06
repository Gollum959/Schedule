import os
from django import forms
from django.core.validators import RegexValidator

from pts_config.models import (PtsConstructor,
                               CameraPtsConstructor,
                               CameraModelBrend,
                               OpticPtsConstructor,
                               OpticModelBrend,
                               ServerRecordingRepeatConstructor,
                               ServerRecordingRepeatModelBrend,
                               MicrophonePtsConstructor,
                               MicrophoneModelBrend,
                               GfxPtsConstructor)


class AddPtsConfigFrom(forms.ModelForm):

    image = forms.FileField()
    name = forms.CharField(
        label='Название конфигурации ПТС',
        validators=[RegexValidator(
            '^[0-9a-zA-ZА-я\s]*$',
            message='Только буквы и цифры'
        )],
        widget=forms.TextInput(attrs={'placeholder': 'Введите имя конфигурации'}),
    )

    def __init__(self, *args, **kwargs):
        self.place_id = kwargs.pop('place', None)
        self.event_id = kwargs.pop('event', None)
        super().__init__(*args, **kwargs)
        self.place_id = self.initial.get('place') if not self.place_id else self.place_id
        self.event_id = self.initial.get('event_type') if not self.event_id else self.event_id
        
        self.__init_and_disable(self.place_id, 'place')
        self.__init_and_disable(self.event_id, 'event_type')
        self.fields['place'].label = 'Название объекта'
        self.fields['event_type'].label = 'Вид события'

    def __init_and_disable(self, field_id, field_name):
        if field_id or self.initial.get(field_name):
            print(field_id)
            self.fields[field_name].initial = field_id
            #self.fields[field_name].disabled = True

    def clean(self):
        cleaned_data = super().clean()
        print(cleaned_data)
        return cleaned_data

    def clean_image(self):
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

    class Meta:
        model = PtsConstructor
        fields = ('place', 'event_type', 'name', 'microphone_quantity', 'image')


class AddCamera(forms.ModelForm):

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['optics'].empty_label = 'Выберете кратность'

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

# class AddCamera(forms.ModelForm):

#     class Meta:
#         model = CameraPtsConstructor
#         fields = ['cameras', 'brend', 'model', 'quantity']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['model'].queryset = CameraModelBrend.objects.none()
#         if 'cameraptsconstructor_set-0-brend' in self.data:
#             try:
#                 self.fields['model'].queryset = CameraModelBrend.objects.all().order_by('name')
#             except (ValueError, TypeError):
#                 pass
#         elif self.instance.pk:
#             # Need to create subscription(in JS) for existing model
#             # self.fields['model'].queryset = CameraModelBrend.objects.filter(brend=self.instance.brend_id).order_by('name') 
#             self.fields['model'].queryset = CameraModelBrend.objects.all().order_by('name') 


# CameraFormset = forms.inlineformset_factory(
#     PtsConstructor, CameraPtsConstructor,
#     form=AddCamera,
#     extra=0,
#     can_delete=True
# )


# class AddOptic(forms.ModelForm):

#     class Meta:
#         model = OpticPtsConstructor
#         fields = ['optics', 'brend', 'model', 'quantity']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['model'].queryset = OpticModelBrend.objects.none()
#         if 'opticptsconstructor_set-0-brend' in self.data:
#             try:
#                 self.fields['model'].queryset = OpticModelBrend.objects.all().order_by('name')
#             except (ValueError, TypeError):
#                 pass
#         elif self.instance.pk:
#             # Need to create subscription(in JS) for existing model
#             # self.fields['model'].queryset = OpticModelBrend.objects.filter(brend=self.instance.brend_id).order_by('name') 
#             self.fields['model'].queryset = OpticModelBrend.objects.all().order_by('name') 


# OpticFormset = forms.inlineformset_factory(
#     PtsConstructor, OpticPtsConstructor,
#     form=AddOptic,
#     extra=0,
#     can_delete=True
# )


# class AddServer(forms.ModelForm):

#     class Meta:
#         model = ServerRecordingRepeatConstructor
#         fields = ['type', 'type_player', 'brend', 'model', 'quantity']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['model'].queryset = ServerRecordingRepeatModelBrend.objects.none()
#         if 'serverrecordingrepeatconstructor_set-0-brend' in self.data:
#             try:
#                 self.fields['model'].queryset = ServerRecordingRepeatModelBrend.objects.all().order_by('name')
#             except (ValueError, TypeError):
#                 pass
#         elif self.instance.pk:
#             # Need to create subscription(in JS) for existing model
#             # self.fields['model'].queryset = ServerRecordingRepeatModelBrend.objects.filter(brend=self.instance.brend_id).order_by('name') 
#             self.fields['model'].queryset = ServerRecordingRepeatModelBrend.objects.all().order_by('name')


# ServerFormset = forms.inlineformset_factory(
#     PtsConstructor, ServerRecordingRepeatConstructor,
#     form=AddServer,
#     extra=0,
#     can_delete=True
# )


# class AddMicrophone(forms.ModelForm):

#     class Meta:
#         model = MicrophonePtsConstructor
#         fields = ['type', 'brend', 'model', 'quantity']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['model'].queryset = MicrophoneModelBrend.objects.none()
#         if 'microphoneptsconstructor_set-0-brend' in self.data:
#             try:
#                 self.fields['model'].queryset = MicrophoneModelBrend.objects.all().order_by('name')
#             except (ValueError, TypeError):
#                 pass
#         elif self.instance.pk:
#             # Need to create subscription(in JS) for existing model
#             # self.fields['model'].queryset = MicrophoneModelBrend.objects.filter(brend=self.instance.brend_id).order_by('name') 
#             self.fields['model'].queryset = MicrophoneModelBrend.objects.all().order_by('name')


# MicroFormset = forms.inlineformset_factory(
#     PtsConstructor, MicrophonePtsConstructor,
#     form=AddMicrophone,
#     extra=0,
#     can_delete=True
# )


# class AddGfx(forms.ModelForm):

#     class Meta:
#         model = GfxPtsConstructor
#         fields = ['gfx', 'model', 'judicial_system',
#                   'license_type', 'quantity']


# GfxFormset = forms.inlineformset_factory(
#     PtsConstructor, GfxPtsConstructor,
#     form=AddGfx,
#     extra=0,
#     can_delete=True
# )
