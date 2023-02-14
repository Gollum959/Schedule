from django.forms import ModelForm, inlineformset_factory

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


class AddPtsConfigFrom(ModelForm):

    class Meta:
        model = PtsConstructor
        fields = ('name', )


class AddCamera(ModelForm):

    class Meta:
        model = CameraPtsConstructor
        fields = ['cameras', 'brend', 'model', 'quantity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['model'].queryset = CameraModelBrend.objects.none()
        if 'cameraptsconstructor_set-0-brend' in self.data:
            try:
                self.fields['model'].queryset = CameraModelBrend.objects.all().order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            # Need to create subscription(in JS) for existing model
            # self.fields['model'].queryset = CameraModelBrend.objects.filter(brend=self.instance.brend_id).order_by('name') 
            self.fields['model'].queryset = CameraModelBrend.objects.all().order_by('name') 


CameraFormset = inlineformset_factory(
    PtsConstructor, CameraPtsConstructor,
    form=AddCamera,
    extra=0,
    can_delete=True
)


class AddOptic(ModelForm):

    class Meta:
        model = OpticPtsConstructor
        fields = ['optics', 'brend', 'model', 'quantity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['model'].queryset = OpticModelBrend.objects.none()
        if 'opticptsconstructor_set-0-brend' in self.data:
            try:
                self.fields['model'].queryset = OpticModelBrend.objects.all().order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            # Need to create subscription(in JS) for existing model
            # self.fields['model'].queryset = OpticModelBrend.objects.filter(brend=self.instance.brend_id).order_by('name') 
            self.fields['model'].queryset = OpticModelBrend.objects.all().order_by('name') 


OpticFormset = inlineformset_factory(
    PtsConstructor, OpticPtsConstructor,
    form=AddOptic,
    extra=0,
    can_delete=True
)


class AddServer(ModelForm):

    class Meta:
        model = ServerRecordingRepeatConstructor
        fields = ['type', 'type_player', 'brend', 'model', 'quantity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['model'].queryset = ServerRecordingRepeatModelBrend.objects.none()
        if 'serverrecordingrepeatconstructor_set-0-brend' in self.data:
            try:
                self.fields['model'].queryset = ServerRecordingRepeatModelBrend.objects.all().order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            # Need to create subscription(in JS) for existing model
            # self.fields['model'].queryset = ServerRecordingRepeatModelBrend.objects.filter(brend=self.instance.brend_id).order_by('name') 
            self.fields['model'].queryset = ServerRecordingRepeatModelBrend.objects.all().order_by('name')


ServerFormset = inlineformset_factory(
    PtsConstructor, ServerRecordingRepeatConstructor,
    form=AddServer,
    extra=0,
    can_delete=True
)


class AddMicrophone(ModelForm):

    class Meta:
        model = MicrophonePtsConstructor
        fields = ['type', 'brend', 'model', 'quantity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['model'].queryset = MicrophoneModelBrend.objects.none()
        if 'microphoneptsconstructor_set-0-brend' in self.data:
            try:
                self.fields['model'].queryset = MicrophoneModelBrend.objects.all().order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            # Need to create subscription(in JS) for existing model
            # self.fields['model'].queryset = MicrophoneModelBrend.objects.filter(brend=self.instance.brend_id).order_by('name') 
            self.fields['model'].queryset = MicrophoneModelBrend.objects.all().order_by('name')


MicroFormset = inlineformset_factory(
    PtsConstructor, MicrophonePtsConstructor,
    form=AddMicrophone,
    extra=0,
    can_delete=True
)


class AddGfx(ModelForm):

    class Meta:
        model = GfxPtsConstructor
        fields = ['gfx', 'model', 'judicial_system',
                  'license_type', 'quantity']


GfxFormset = inlineformset_factory(
    PtsConstructor, GfxPtsConstructor,
    form=AddGfx,
    extra=0,
    can_delete=True
)
