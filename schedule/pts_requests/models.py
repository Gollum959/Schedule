from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse

from users.models import User
from pts_config.models import PtsConstructor
from place_broadcast.models import PlaceConstructor, EventType
from pts_requests.abstract_models import NameModel, LineConstructor


class BroadCastType(NameModel):
    """Type of the broadcast(live, recording, test)"""


class PtsName(NameModel):
    """Names and teams of PTS"""
    head_fullname = models.CharField(
        'ФИО Начальника смены ПТС',
        max_length=70
    )
    head_contact = models.CharField(
        'Контактный телефон  Начальника смены ПТС',
        max_length=100
    )
    deputi_head_fullname = models.CharField(
        'ФИО Заместителя начальника смены ПТС',
        max_length=70
    )
    deputi_head_contact = models.CharField(
        'Контактный телефон  Заместителя Начальника смены ПТС',
        max_length=100
    )
    other_information = models.TextField(
        'Примечание',
        max_length=2000,
        blank=True)


class CommLineConstructor(LineConstructor):
    """Line of communication model."""

    start = models.DateTimeField(
        verbose_name='Дата и время начала',
        help_text='Дата и время начала трансляции(YYYY-MM-DD hh:mm)',
    )
    end = models.DateTimeField(
        verbose_name='Дата и время окончания',
        help_text='Дата и время окончания трансляции(YYYY-MM-DD hh:mm)',
    )

    quantity = models.PositiveSmallIntegerField(
        'Количество',
        validators=(
            MinValueValidator(0),
            MaxValueValidator(25),
        ),
        default=0,
    )


class PlaceInsideBT(models.Model):
    """Places inside BT like AVZ4 or S300"""

    name = models.CharField(
        'Аппаратная',
        max_length=50,
    )


class TechCommLineConstructor(models.Model):
    """Line of technical communication model."""

    FOUR_WIRE_COMM = 'four'
    VPN = 'vpn'
    COMM_TYPE = [
        (FOUR_WIRE_COMM, 'Четырех проводка'),
        (VPN, 'VPN'),
    ]

    type = models.CharField(
        verbose_name='Тип связи',
        max_length=30,
        choices=COMM_TYPE,
    )
    quantity = models.PositiveSmallIntegerField(
        'Количество',
        validators=(
            MinValueValidator(0),
            MaxValueValidator(25),
        ),
        default=0,
    )
    place = models.ForeignKey(
        'PlaceInsideBT',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    pts_request = models.ForeignKey(
        'PtsRequest',
        on_delete=models.CASCADE,
    )


class PtsRequest(models.Model):
    """Broadcast request model."""
    ONE_HEADSEAT = 'one'
    TWO_HEADSEAT = 'two'
    HEADSEAT = [
        (ONE_HEADSEAT, 'Одна ганитура'),
        (TWO_HEADSEAT, 'Две гарнитуры'),
    ]
    APPROVED = 'approved'
    REJECTED = 'rejected'
    ON_APPROVAL = 'approval'
    UNDER_REVISION = 'revision'
    STATUS = [
        (APPROVED, 'Утверждено'),
        (REJECTED, 'Отклонено'),
        (ON_APPROVAL, 'На утверждении'),
        (UNDER_REVISION, 'На доработке'),
    ]

    name = models.CharField(
        'Название Трансляции',
        max_length=200,
    )

    broadcast_start_date = models.DateTimeField(
        verbose_name='Дата и время начала трансляции',
        help_text='Дата и время начала трансляции(YYYY-MM-DD hh:mm)',
    )
    broadcast_end_date = models.DateTimeField(
        verbose_name='Дата и время окончания трансляции',
        help_text='Дата и время окончания трансляции(YYYY-MM-DD hh:mm)',
    )
    place = models.ForeignKey(
        PlaceConstructor,
        on_delete=models.CASCADE,
        verbose_name='Площадка',
    )
    event_type = models.ForeignKey(
        EventType,
        on_delete=models.CASCADE,
        verbose_name='Вид события'
    )
    type = models.ForeignKey(
        BroadCastType,
        on_delete=models.CASCADE,
        verbose_name='Тип работы'
    )
    start_date = models.DateTimeField(
        verbose_name='Дата и время выезда ПТС',
        help_text='Дата и время выезда ПТС (YYYY-MM-DD hh:mm)',
        blank=True,
        null=True
    )
    end_date = models.DateTimeField(
        verbose_name='Дата и время отьезда ПТС',
        help_text='Дата и время отьезда ПТС (YYYY-MM-DD hh:mm)',
        blank=True,
        null=True
    )
    trakt_start_date = models.DateTimeField(
        verbose_name='Дата и время начала тракта',
        help_text='Дата и время начала тракта (YYYY-MM-DD hh:mm)',
        blank=True,
        null=True
    )
    trakt_end_date = models.DateTimeField(
        verbose_name='Дата и время окончания тракта',
        help_text='Дата и время окончания тракта (YYYY-MM-DD hh:mm)',
        blank=True,
        null=True
    )
    pts_name = models.ManyToManyField(
        PtsName,
        blank=True,
    )
    pts_cfg = models.ForeignKey(
        PtsConstructor,
        on_delete=models.CASCADE,
        verbose_name='Конфигурация ПТС',
    )
    commentator_monitor = models.BooleanField(
        'Комментаторский монитор',
        default=False
    )
    commentator_console = models.BooleanField(
        'Комментаторская панель',
        default=False
    )
    commentator_headset = models.CharField(
        verbose_name='Количество комментаторских гарнитур',
        max_length=30,
        choices=HEADSEAT,
        blank=True,
        null=True
    )
    status = models.CharField(
        verbose_name='Статус Заявки',
        max_length=30,
        choices=STATUS,
        default=ON_APPROVAL
    )
    # image = models.ImageField(
    #     'Картинка или pdf',
    #     upload_to='plans/',
    #     blank=True
    # )
    comment = models.TextField(
        'Комментарий к Заявке',
        max_length=2000,
        blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    def get_absolute_url(self):
        return reverse('pts_requests:request_detail', kwargs={"pk": self.pk})

    def get_pts(self):
        return ", ".join([pts.name for pts in self.pts_name.all()])

    @property
    def is_approval(self):
        """Return True if status is ON APPROVAL."""
        return self.status == self.ON_APPROVAL

    class Meta:
        verbose_name = 'Заявка ПТС'
        verbose_name_plural = 'Заявка ПТС'
        ordering = ('broadcast_start_date', )
