from django.db import models

from pts_config.abstract_models import StrName, ConstrQuantity
from users.models import User


class Camera(StrName):
    """Camera type model."""
    name = models.CharField('Type of cameras', max_length=20)


class CameraBrend(StrName):
    """Camera brend model."""
    name = models.CharField('Camera brend', max_length=20)


class CameraModelBrend(StrName):
    """Model camera model connected with CameraBrend model"""
    name = models.CharField('Camera model', max_length=20)
    brend = models.ForeignKey(
        CameraBrend,
        on_delete=models.CASCADE,
    )


class CameraPtsConstructor(ConstrQuantity):
    """Many2many model for PtsConstructor and Camera."""

    cameras = models.ForeignKey(
        'Camera',
        on_delete=models.CASCADE,
        verbose_name='Camera type'
    )
    brend = models.ForeignKey(
        'CameraBrend',
        on_delete=models.CASCADE,
    )
    model = models.ForeignKey(
        'CameraModelBrend',
        on_delete=models.CASCADE,
    )


class Optic(StrName):
    """Optics type model."""
    name = models.CharField('Optical magnification', max_length=20)


class OpticBrend(StrName):
    """Optic brend model."""
    name = models.CharField('Optic brend', max_length=20)


class OpticModelBrend(StrName):
    """Optics model model connected with OpticBrend model"""
    name = models.CharField('Optic model', max_length=20)
    brend = models.ForeignKey(
        OpticBrend,
        on_delete=models.CASCADE,
    )


class OpticPtsConstructor(ConstrQuantity):
    """Many2many model for PtsConstructor and Optic."""

    optics = models.ForeignKey(
        'Optic',
        on_delete=models.CASCADE,
        verbose_name='Optical magnification'
    )
    brend = models.ForeignKey(
        'OpticBrend',
        on_delete=models.CASCADE,
    )
    model = models.ForeignKey(
        'OpticModelBrend',
        on_delete=models.CASCADE,
    )


class ServerRecordingRepeatBrend(StrName):
    """Server recording or repeat model."""
    name = models.CharField('Server brend', max_length=20)


class ServerRecordingRepeatModelBrend(StrName):
    """Server model model connected with ServerRecordingRepeatBrend model"""
    name = models.CharField('Server model', max_length=20)
    brend = models.ForeignKey(
        ServerRecordingRepeatBrend,
        on_delete=models.CASCADE,
    )


class ServerPlayerType(StrName):
    """Server player type model"""
    RECORDING = 'recording'
    REPEAT = 'repeat'
    TYPE = [
        (RECORDING, 'Сервер записи'),
        (REPEAT, 'Сервер повтора'),
    ]
    name = models.CharField('Server player type', max_length=40)
    type = models.CharField(
        verbose_name='Server type',
        max_length=20,
        choices=TYPE,
    )


class ServerRecordingRepeatConstructor(ConstrQuantity):
    """Many2many model for PtsConstructor and ServerRecordingRepeat."""

    RECORDING = 'recording'
    REPEAT = 'repeat'
    TYPE = [
        (RECORDING, 'Сервер записи'),
        (REPEAT, 'Сервер повтора'),
    ]

    type = models.CharField(
        verbose_name='Server type',
        max_length=20,
        choices=TYPE,
        blank=True,
        default=None,
    )
    type_player = models.ForeignKey(
        'ServerPlayerType',
        on_delete=models.CASCADE,
        blank=True
    )
    brend = models.ForeignKey(
        'ServerRecordingRepeatBrend',
        on_delete=models.CASCADE,
        blank=True
    )
    model = models.ForeignKey(
        'ServerRecordingRepeatModelBrend',
        on_delete=models.CASCADE,
        blank=True
    )


class MicrophoneBrend(StrName):
    """Microphone brend model."""
    name = models.CharField('Type of microphones', max_length=20)


class MicrophoneModelBrend(StrName):
    """Microphones model model connected with OpticBrend model"""
    name = models.CharField('Microphone model', max_length=20)
    brend = models.ForeignKey(
        MicrophoneBrend,
        on_delete=models.CASCADE,
    )


class MicrophonePtsConstructor(ConstrQuantity):
    """Many2many model for PtsConstructor and Microphone."""
    GUN = 'gun'
    HALF_GUN = 'half_gun'
    HAND_STEREO = 'hand_stereo'
    TYPE = [
        (GUN, 'Пушка'),
        (HALF_GUN, 'Полупушка'),
        (HAND_STEREO, 'Ручной стерео'),
    ]

    type = models.CharField(
        verbose_name='Micro type',
        max_length=20,
        choices=TYPE,
    )
    brend = models.ForeignKey(
        'MicrophoneBrend',
        on_delete=models.CASCADE,
    )
    model = models.ForeignKey(
        'MicrophoneModelBrend',
        on_delete=models.CASCADE,
    )


class Gfx(StrName):
    """Graphic stations type model."""
    name = models.CharField('Graphic stations', max_length=20)


class GfxModel(StrName):
    """Graphic model model connected with Gfx model"""
    name = models.CharField('GFX model', max_length=20)
    type = models.ForeignKey(
        Gfx,
        on_delete=models.CASCADE,
    )


class GfxLicenseType(StrName):
    """Graphic stations, license type."""
    name = models.CharField('License type(kind of sport)', max_length=20)


class GfxPtsConstructor(ConstrQuantity):
    """Many2many model for PtsConstructor and Gfx."""

    gfx = models.ForeignKey(
        'Gfx',
        on_delete=models.CASCADE,
        related_name='gfx',
    )
    model = models.ForeignKey(
        'GfxModel',
        on_delete=models.CASCADE,
    )
    judicial_system = models.BooleanField(
        default=False
    )
    license_type = models.ManyToManyField(
        'GfxLicenseType',
        blank=True,
    )


class PtsConstructor(models.Model):
    """PTS configuration model."""

    name = models.CharField('PTS config name', max_length=30, unique=True)
    optics = models.ManyToManyField(
        'Optic',
        through='OpticPtsConstructor',
        blank=True
    )
    cameras = models.ManyToManyField(
        'Camera',
        through='CameraPtsConstructor',
        blank=True
    )
    servers = models.ManyToManyField(
        'ServerRecordingRepeatConstructor',
    )
    microphones = models.ManyToManyField(
        'MicrophonePtsConstructor',
    )
    gfxs = models.ManyToManyField(
        'Gfx',
        through='GfxPtsConstructor',
        blank=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.name}'

    class Meta:
        verbose_name = 'PTS config'
        verbose_name_plural = 'PTS configs'
        ordering = ('create_date', )
