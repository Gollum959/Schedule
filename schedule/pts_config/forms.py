from django.forms import ModelForm, inlineformset_factory

from pts_config.models import (PtsConstructor,
                               CameraPtsConstructor,
                               OpticPtsConstructor,
                               ServerRecordingRepeatConstructor,
                               MicrophonePtsConstructor,
                               GfxPtsConstructor)


class AddPtsConfigFrom(ModelForm):

    class Meta:
        model = PtsConstructor
        fields = ('name', )


class AddCamera(ModelForm):

    class Meta:
        model = CameraPtsConstructor
        fields = ['cameras', 'brend', 'model', 'quantity']


CameraFormset = inlineformset_factory(
    PtsConstructor, CameraPtsConstructor,
    form=AddCamera,
    extra=2,
    can_delete=True
)


class AddOptic(ModelForm):

    class Meta:
        model = OpticPtsConstructor
        fields = ['optics', 'brend', 'model', 'quantity']


OpticFormset = inlineformset_factory(
    PtsConstructor, OpticPtsConstructor,
    form=AddOptic,
    extra=2,
    can_delete=True
)


class AddServer(ModelForm):

    class Meta:
        model = ServerRecordingRepeatConstructor
        fields = ['type', 'type_player', 'brend', 'model', 'quantity']


ServerFormset = inlineformset_factory(
    PtsConstructor, ServerRecordingRepeatConstructor,
    form=AddServer,
    extra=2,
    can_delete=True
)


class AddMicrophone(ModelForm):

    class Meta:
        model = MicrophonePtsConstructor
        fields = ['type', 'brend', 'model', 'quantity']


MicroFormset = inlineformset_factory(
    PtsConstructor, MicrophonePtsConstructor,
    form=AddMicrophone,
    extra=2,
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
    extra=2,
    can_delete=True
)
