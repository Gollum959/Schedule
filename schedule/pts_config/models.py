from django.db import models

from pts_config.abstract_models import StrName, ConstrQuantity


class Optic(StrName):
    """Optics type model."""

    name = models.CharField('Type of optics', max_length=30)


class OpticPtsConstructor(ConstrQuantity):
    """Many2many model for PtsConstructor and Optic."""

    optics = models.ForeignKey(
        'Optics',
        on_delete=models.CASCADE,
    )


class Camera(StrName):
    """Cameras type model."""

    name = models.CharField('Type of cameras', max_length=20)


class CameraPtsConstructor(ConstrQuantity):
    """Many2many model for PtsConstructor and Camera."""

    cameras = models.ForeignKey(
        'Cameras',
        on_delete=models.CASCADE,
    )


class Microphone(StrName):
    """Microphones type model."""

    name = models.CharField('Type of microphones', max_length=50)


class MicrophonePtsConstructor(ConstrQuantity):
    """Many2many model for PtsConstructor and Microphone."""

    microphones = models.ForeignKey(
        'Microphones',
        on_delete=models.CASCADE,
    )


class Commentator(StrName):
    """Commentator equipment type model."""

    name = models.CharField('Type of commentary equipment', max_length=30)


class CommentatorPtsConstructor(ConstrQuantity):
    """Many2many model for PtsConstructor and Commentator."""

    commentators = models.ForeignKey(
        'Commentators',
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

    def __str__(self) -> str:
        return f'{self.name}'

    class Meta:
        verbose_name = 'PTS config'
        verbose_name_plural = 'PTS configs'
        ordering = ('name', )
