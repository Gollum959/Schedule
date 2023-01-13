from django.contrib import admin

from pts_config.models import (
    PtsConstructor,
    Camera, CameraPtsConstructor,
    Optic, OpticPtsConstructor,
    Microphone, MicrophonePtsConstructor,
    Commentator, CommentatorPtsConstructor,
    Gfx, GfxPtsConstructor
)


@admin.register(Camera, Optic, Microphone, Commentator, Gfx)
class CameraAdmin(admin.ModelAdmin):
    """Displaying Camera, Optic, Microphone, Commentator, Gfx
       model in the admin panel."""
    list_display = ('name', )


class CameraPtsConstructorInline(admin.TabularInline):
    """Display camera in PTS config."""

    model = CameraPtsConstructor
    extra = 1


class OpticPtsConstructor(admin.TabularInline):
    """Display optic in PTS config."""

    model = OpticPtsConstructor
    extra = 1


class MicrophonePtsConstructor(admin.TabularInline):
    """Display microphone in PTS config."""

    model = MicrophonePtsConstructor
    extra = 1


class CommentatorPtsConstructor(admin.TabularInline):
    """Display comentator equipment in PTS config."""

    model = CommentatorPtsConstructor
    extra = 1


class GfxPtsConstructor(admin.TabularInline):
    """Display GFX in PTS config."""

    model = GfxPtsConstructor
    extra = 1


@admin.register(PtsConstructor)
class PtsConstructorAdmin(admin.ModelAdmin):
    """Displaying the PtsConstructor model in the admin panel."""

    list_display = ('name', )
    search_fields = ('name', )
    inlines = (
        CameraPtsConstructorInline,
        OpticPtsConstructor,
        MicrophonePtsConstructor,
        CommentatorPtsConstructor,
        GfxPtsConstructor
    )
