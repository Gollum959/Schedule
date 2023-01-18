from django.db import models

from pts_config.abstract_models import StrName, ConstrQuantity, StrNameModel
from users.models import User


class Camera(StrNameModel):
    """Camera type model."""
    description = 'Type of cameras'


class CameraBrend(StrNameModel):
    """Camera brend model."""
    description = 'Camera brend'


class CameraModelBrend(StrNameModel):
    """Model camera model connected with CameraBrend model"""
    description = 'Camera model'

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
        blank=True
    )
    model = models.ForeignKey(
        'CameraModelBrend',
        on_delete=models.CASCADE,
        blank=True
    )


class Optic(StrNameModel):
    """Optics type model."""
    description = 'Optical magnification'


class OpticBrend(StrNameModel):
    """Optic brend model."""
    description = 'Optic brend'


class OpticModelBrend(StrNameModel):
    """Optics model model connected with OpticBrend model"""
    description = 'Optic model'

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
        blank=True
    )
    model = models.ForeignKey(
        'OpticModelBrend',
        on_delete=models.CASCADE,
        blank=True
    )





class Microphone(StrName):
    """Microphones type model."""

    name = models.CharField('Type of microphones', max_length=50)


class MicrophonePtsConstructor(ConstrQuantity):
    """Many2many model for PtsConstructor and Microphone."""

    microphones = models.ForeignKey(
        'Microphone',
        on_delete=models.CASCADE,
    )


class Commentator(StrName):
    """Commentator equipment type model."""

    name = models.CharField('Type of commentary equipment', max_length=30)


class CommentatorPtsConstructor(ConstrQuantity):
    """Many2many model for PtsConstructor and Commentator."""

    commentators = models.ForeignKey(
        'Commentator',
        on_delete=models.CASCADE,
    )


class Gfx(StrName):
    """Graphic stations type model."""

    name = models.CharField('Graphic stations', max_length=30)


class GfxPtsConstructor(ConstrQuantity):
    """Many2many model for PtsConstructor and Gfx."""

    gfx = models.ForeignKey(
        'Gfx',
        on_delete=models.CASCADE,
        related_name='gfx',
    )


class PtsConstructor(models.Model):
    """PTS configuration model."""

    name = models.CharField('PTS config name', max_length=30, unique=True)
    optics = models.ManyToManyField(
        'Optic',
        through='OpticPtsConstructor',
    )
    cameras = models.ManyToManyField(
        'Camera',
        through='CameraPtsConstructor',
    )
    microphones = models.ManyToManyField(
        'Microphone',
        through='MicrophonePtsConstructor',
    )
    commentators = models.ManyToManyField(
        'Commentator',
        through='CommentatorPtsConstructor',
    )
    gfxs = models.ManyToManyField(
        'Gfx',
        through='GfxPtsConstructor',
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
