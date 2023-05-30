from django.db import models
from django.urls import reverse
from django.db.models import Q
from django.core.validators import MaxValueValidator, MinValueValidator

from pts_config.abstract_models import StrName, ConstrQuantity, StrNameQuantity
from users.models import User
from place_broadcast.models import EventType, PlaceConstructor


class TypePtsForConfiguration(StrName):
    """PTS type model."""
    name = models.CharField('Type of PTS', max_length=50)


class Camera(StrName):
    """Camera type model."""
    name = models.CharField('Type of cameras', max_length=50)


class CameraBrend(StrName):
    """Camera brend model."""
    name = models.CharField('Camera brend', max_length=50)
    type_pts = models.ForeignKey(
        TypePtsForConfiguration,
        on_delete=models.CASCADE,
        help_text="If this brand can be used everywhere, choose nothing",
        blank=True,
        null=True
    )


class CameraModelBrend(StrNameQuantity):
    """Model camera model connected with CameraBrend model"""
    name = models.CharField('Camera model', max_length=50)
    brend = models.ForeignKey(
        CameraBrend,
        on_delete=models.CASCADE,
    )
    type = models.ForeignKey(
        Camera,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )


class CameraPtsConstructor(ConstrQuantity):
    """Model for PtsConstructor and Camera."""

    cameras = models.ForeignKey(
        'Camera',
        on_delete=models.CASCADE,
        verbose_name='Тип Камеры'
    )
    brend = models.ForeignKey(
        'CameraBrend',
        on_delete=models.CASCADE,
        verbose_name='Производитель камеры',
        blank=True,
        null=True
    )
    model = models.ForeignKey(
        'CameraModelBrend',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )


class Optic(StrName):
    """Optics type model."""
    name = models.CharField('Optical magnification', max_length=50)
    visible_to_user = models.BooleanField(
        'Видят ли пользователи',
        default=False
    )


class OpticBrend(StrName):
    """Optic brend model."""
    name = models.CharField('Optic brend', max_length=50)
    type_pts = models.ForeignKey(
        TypePtsForConfiguration,
        on_delete=models.CASCADE,
        help_text="If this brand can be used everywhere, choose nothing",
        blank=True,
        null=True
    )


class OpticModelBrend(StrNameQuantity):
    """Optics model model connected with OpticBrend model"""
    name = models.CharField('Optic model', max_length=50)
    brend = models.ForeignKey(
        OpticBrend,
        on_delete=models.CASCADE,
    )
    type = models.ForeignKey(
        Optic,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )


class OpticPtsConstructor(ConstrQuantity):
    """Model for PtsConstructor and Optic."""

    optics = models.ForeignKey(
        'Optic',
        on_delete=models.CASCADE,
        verbose_name='Кратность Оптики'
    )
    brend = models.ForeignKey(
        'OpticBrend',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    model = models.ForeignKey(
        'OpticModelBrend',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )


class ServerRecordingRepeatType(StrName):
    """Server type model."""
    name = models.CharField('Server type', max_length=50)


class ServerPlayerType(StrName):
    """Server player type model"""
    name = models.CharField('Server player type', max_length=40)
    rec_rep_type = models.ForeignKey(
        ServerRecordingRepeatType,
        on_delete=models.CASCADE,
    )
    visible_to_user = models.BooleanField(
        'Видят ли пользователи',
        default=False
    )


class ServerRecordingRepeatBrend(StrName):
    """Server recording or repeat brend model."""
    name = models.CharField('Server brend', max_length=50)
    type_pts = models.ForeignKey(
        TypePtsForConfiguration,
        on_delete=models.CASCADE,
        help_text="If this brand can be used everywhere, choose nothing",
        blank=True,
        null=True
    )


class ServerRecordingRepeatModelBrend(StrNameQuantity):
    """Server model model connected with ServerRecordingRepeatBrend model"""
    name = models.CharField('Server model', max_length=50)
    brend = models.ForeignKey(
        ServerRecordingRepeatBrend,
        on_delete=models.CASCADE,
    )


class ServerRecordingRepeatConstructor(ConstrQuantity):
    """Model for PtsConstructor and ServerRecordingRepeat."""

    type = models.ForeignKey(
        'ServerRecordingRepeatType',
        on_delete=models.CASCADE,
    )
    type_player = models.ForeignKey(
        'ServerPlayerType',
        on_delete=models.CASCADE,
    )
    brend = models.ForeignKey(
        'ServerRecordingRepeatBrend',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    model = models.ForeignKey(
        'ServerRecordingRepeatModelBrend',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )


class MicrophoneType(StrName):
    """Microphone type model."""
    name = models.CharField('Type of microphones', max_length=50)


class MicrophoneBrend(StrName):
    """Microphone brend model."""
    name = models.CharField('Type of microphones', max_length=50)


class MicrophoneModelBrend(StrNameQuantity):
    """Microphones model model connected with OpticBrend model"""
    name = models.CharField('Microphone model', max_length=50)
    brend = models.ForeignKey(
        MicrophoneBrend,
        on_delete=models.CASCADE,
    )
    type_micro = models.ForeignKey(
        MicrophoneType,
        on_delete=models.CASCADE,
    )
    type_pts = models.ForeignKey(
        TypePtsForConfiguration,
        on_delete=models.CASCADE,
        help_text="If this brand can be used everywhere, choose nothing",
        blank=True,
        null=True
    )


class MicrophonePtsConstructor(ConstrQuantity):
    """Model for PtsConstructor and Microphone."""

    type = models.ForeignKey(
        'MicrophoneType',
        on_delete=models.CASCADE,
    )
    brend = models.ForeignKey(
        'MicrophoneBrend',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    model = models.ForeignKey(
        'MicrophoneModelBrend',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )


class Gfx(StrName):
    """Graphic stations type model."""
    name = models.CharField('Graphic stations', max_length=50)


class GfxModel(StrNameQuantity):
    """Graphic model model connected with Gfx model"""
    name = models.CharField('GFX model', max_length=50)
    type = models.ForeignKey(
        Gfx,
        on_delete=models.CASCADE,
    )


class GfxLicenseType(StrName):
    """Graphic stations, license type."""
    name = models.CharField('License type(kind of sport)', max_length=50)


class GfxPtsConstructor(ConstrQuantity):
    """Model for PtsConstructor and Gfx."""

    gfx = models.ForeignKey(
        'Gfx',
        on_delete=models.CASCADE,
        related_name='gfx',
    )
    model = models.ForeignKey(
        'GfxModel',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    judicial_system = models.BooleanField(
        'Подключение к судейской системе?',
        default=False
    )
    license_type = models.ManyToManyField(
        'GfxLicenseType',
        blank=True,
    )
    quantity = models.PositiveSmallIntegerField(
        'Количество',
        validators=(
            MinValueValidator(1),
            MaxValueValidator(50),
        ),
        default=1,
    )

    @property
    def get_license_type(self):
        return ", ".join(
            [license_type.name for license_type in self.license_type.all()]
        )


class PtsConstructor(models.Model):
    """PTS configuration model."""

    name = models.CharField(
        'Название конфигурации ПТС',
        max_length=50,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    event_type = models.ForeignKey(
        EventType,
        on_delete=models.CASCADE,
    )
    place = models.ForeignKey(
        PlaceConstructor,
        on_delete=models.CASCADE,
    )
    base_conf = models.BooleanField(
        'Базовая комплектация',
        default=False
    )
    clone_conf = models.BooleanField(
        'Комплектация привязаная к заявке',
        default=False
    )
    microphone_quantity = models.PositiveSmallIntegerField(
        'Количество',
        validators=(
            MinValueValidator(1),
            MaxValueValidator(30),
        ),
        default=0,
        blank=True
    )
    microphone_comment = models.TextField(
        'Комментарий к заказу микрофонов',
        max_length=2000,
        blank=True)
    image = models.ImageField(
        'Картинка или pdf',
        upload_to='plans/',
        blank=True
    )
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('config:config_detail', kwargs={'pk': self.pk})

    @property
    def get_base_name(self):
        """Add string to configuration name if it's base"""
        return f'{self.name}. Базовая' if self.base_conf else f'{self.name}'

    class Meta:
        verbose_name = 'Конфигурация ПТС'
        verbose_name_plural = 'PTS configs'
        ordering = ('create_date', )
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'author'],
                condition=Q(clone_conf=False, base_conf=False),
                name='unique_name_for_not_clone'
            ),
            models.UniqueConstraint(
                fields=['event_type', 'place', 'author'],
                condition=Q(base_conf=True),
                name='one_base_cfg_to_event_place_author'
            ),

        ]
