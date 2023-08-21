from django.contrib import admin

from pts_config.models import (
    PtsConstructor,
    Camera, CameraBrend, CameraModelBrend, CameraPtsConstructor,
    Optic, OpticBrend, OpticModelBrend, OpticPtsConstructor,
    MicrophoneBrend, MicrophoneModelBrend, MicrophonePtsConstructor,
    MicrophoneType,
    Gfx, GfxPtsConstructor, GfxModel, GfxLicenseType,
    ServerRecordingRepeatBrend, ServerRecordingRepeatModelBrend,
    ServerRecordingRepeatConstructor, ServerPlayerType,
    ServerRecordingRepeatType, TypePtsForConfiguration,
    ImageBank
)


@admin.register(Camera, Optic,
                MicrophoneBrend, MicrophoneModelBrend, MicrophoneType,
                Gfx, GfxModel, GfxLicenseType, CameraBrend,
                CameraModelBrend, OpticBrend, OpticModelBrend,
                ServerRecordingRepeatBrend, ServerRecordingRepeatModelBrend,
                ServerPlayerType, ServerRecordingRepeatType,
                TypePtsForConfiguration)
class CameraAdmin(admin.ModelAdmin):
    """Displaying Camera, Optic, Microphone, Commentator, Gfx
       model and other in the admin panel."""
    list_display = ('name', )


class CameraPtsConstructorInline(admin.TabularInline):
    """Display camera in PTS config."""

    model = CameraPtsConstructor
    fields = ('cameras', 'brend', 'model', 'quantity')
    extra = 1


class OpticPtsConstructor(admin.TabularInline):
    """Display optic in PTS config."""

    model = OpticPtsConstructor
    fields = ['optics', 'brend', 'model', 'quantity']
    extra = 1


class ServerRecordingRepeatConstructor(admin.TabularInline):
    """Display optic in PTS config."""

    model = ServerRecordingRepeatConstructor
    fields = ['type', 'type_player', 'brend', 'model', 'quantity']
    extra = 1


class MicrophonePtsConstructor(admin.TabularInline):
    """Display microphone in PTS config."""

    model = MicrophonePtsConstructor
    fields = ['type', 'brend', 'model', 'quantity']
    extra = 1


class GfxPtsConstructor(admin.TabularInline):
    """Display GFX in PTS config."""

    model = GfxPtsConstructor
    fields = ['gfx', 'model', 'judicial_system', 'license_type', 'quantity']
    extra = 1


@admin.register(PtsConstructor)
class PtsConstructorAdmin(admin.ModelAdmin):
    """Displaying the PtsConstructor model in the admin panel."""

    fields = ('name', 'author', 'place',
              'event_type', 'base_conf',
              'clone_conf', 'image', 'microphone_quantity')
    list_display = ('name', 'author')
    list_filter = ('author', 'clone_conf',)
    search_fields = ('name', )
    inlines = (
        CameraPtsConstructorInline,
        OpticPtsConstructor,
        ServerRecordingRepeatConstructor,
        MicrophonePtsConstructor,
        GfxPtsConstructor
    )


admin.site.register(ImageBank)
