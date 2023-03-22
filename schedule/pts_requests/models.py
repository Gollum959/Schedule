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
    """Communication line model."""

    DIRECTION_TO = 'to_pts'
    DIRECTION_FROM = 'from_pts'
    DIRECTION_CUSTOM = 'custom'
    DIRECTION = [
        (DIRECTION_TO, 'От ЦА к ПТС'),
        (DIRECTION_FROM, 'От ПТС к ЦА'),
        (DIRECTION_CUSTOM, 'Другое'),
    ]
    custom = models.CharField(
        'Ваше направление',
        max_length=200,
        blank=True
    )
    direction = models.CharField(
        verbose_name='Направление',
        max_length=20,
        choices=DIRECTION,
    )


class PlaceInsideBT(models.Model):
    """Places inside BT like AVZ4 or S300"""

    name = models.CharField(
        'Аппаратная',
        max_length=50,
    )

    def __str__(self) -> str:
        return f'{self.name}'


class TechCommLineConstructor(LineConstructor):
    """Technical line communication model."""

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
    place = models.ForeignKey(
        'PlaceInsideBT',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )


class InternetLineConstructor(LineConstructor):
    """Internet line communication model."""

    SPEED1 = '1'
    SPEED2 = '2'
    SPEED3 = '3'
    COMM_TYPE = [
        (SPEED1, '20/20 Мбит/c'),
        (SPEED2, '80/40 Мбит/c'),
        (SPEED3, '200/200 Мбит/c'),
    ]

    speed = models.CharField(
        verbose_name='Скорость соединения',
        max_length=30,
        choices=COMM_TYPE,
    )


class PtsRequest(models.Model):
    """Broadcast request model."""
    ONE_HEADSEAT = 'one'
    TWO_HEADSEAT = 'two'
    HEADSEAT = [
        (ONE_HEADSEAT, 'Одна ганитура'),
        (TWO_HEADSEAT, 'Две гарнитуры'),
    ]
    DRAFT = 'draft'
    APPROVED = 'approved'
    REJECTED = 'rejected'
    ON_APPROVAL = 'approval'
    UNDER_REVISION = 'revision'
    STATUS = [
        (DRAFT, 'Черновик'),
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
        on_delete=models.RESTRICT,
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
        on_delete=models.RESTRICT,
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
        default=DRAFT
    )
    comment = models.TextField(
        'Комментарий к Заявке',
        max_length=2000,
        blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    @staticmethod
    def crete_clone(obj):
        related_fields = [obj.cameraptsconstructor_set.all(),
                          obj.opticptsconstructor_set.all(),
                          obj.serverrecordingrepeatconstructor_set.all(),
                          obj.gfxptsconstructor_set.all()]
        clone = obj._meta.model.objects.get(pk=obj.pk)
        clone.pk = None
        clone.clone_conf = True
        clone.base_conf = False
        clone.save()
        for related_field in related_fields:
            if related_field:
                for field in related_field:
                    field.pk = None
                    field.constructor = clone
                    field.save()

        return clone

    # @staticmethod
    # def delete_clone(id_request):
    #     old_request = PtsRequest.objects.get(pk=id_request)
    #     if old_request.pts_cfg.clone_conf:
    #         old_request.pts_cfg.delete()

    def save(self, *args, **kwargs):
        old_request = PtsRequest.objects.get(pk=self.pk) if self.pk else None
        if ((not self.pk) or (old_request and old_request.pts_cfg != self.pts_cfg)):
            self.pts_cfg = self.crete_clone(self.pts_cfg)
        old_pts_cfg = old_request.pts_cfg if old_request and old_request.pts_cfg != self.pts_cfg else None
        super().save(*args, **kwargs)
        if old_pts_cfg:
            old_pts_cfg.delete()

    def get_absolute_url(self):
        return reverse('pts_requests:request_detail', kwargs={"pk": self.pk})

    @property
    def get_pts(self):
        return ", ".join([pts.name for pts in self.pts_name.all()])

    @property
    def is_approval(self):
        """Return True if status is ON APPROVAL."""
        return self.status == self.ON_APPROVAL

    @property
    def is_draft(self):
        """Return True if status is DRAFT."""
        return self.status == self.DRAFT

    @property
    def is_draft_or_reject(self):
        """Return True if status is ON APPROVAL."""
        return (self.status == self.DRAFT or self.status == self.REJECTED)

    class Meta:
        verbose_name = 'Заявка ПТС'
        verbose_name_plural = 'Заявка ПТС'
        ordering = ('broadcast_start_date', )
