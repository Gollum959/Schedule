from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse

from users.models import User
from pts_config.models import PtsConstructor
from place_broadcast.models import PlaceConstructor
from pts_requests.abstract_models import NameModel, LineConstructor


class BroadCastType(NameModel):
    """Type of the broadcast(live, recording, test)"""


class PtsName(NameModel):
    """Names and teams of PTS"""
    head_fullname = models.CharField(
        'Full name of the head of the PTS shift',
        max_length=70
    )
    head_contact = models.CharField(
        'Contact of the head of the PTS shift',
        max_length=100
    )
    deputi_head_fullname = models.CharField(
        'Full name of the deputy head of the PTS shift',
        max_length=70
    )
    deputi_head_contact = models.CharField(
        'Contact of the deputy head of the PTS shift',
        max_length=100
    )
    other_informatio = models.TextField(
        'Other information',
        max_length=2000,
        blank=True)


class CommLineConstructor(LineConstructor):
    """Line of communication model."""
    internet = models.BooleanField(
        'The Internet yes or no',
        default=False
    )
    quantity = models.PositiveSmallIntegerField(
        'Quantity',
        validators=(
            MinValueValidator(0),
            MaxValueValidator(25),
        ),
        default=0,
    )


class TechCommLineConstructor(LineConstructor):
    """Line of technical communication model."""
    four_wire_comm = models.BooleanField(
        'Four wire communication yes or no',
        default=False
    )
    vpn = models.BooleanField(
        'VPN communication yes or no',
        default=False
    )


class PtsRequest(models.Model):
    """Broadcast request model."""
    ONE_HEADSEAT = 'one'
    TWO_HEADSEAT = 'two'
    HEADSEAT = [
        (ONE_HEADSEAT, 'Одна ганитура'),
        (TWO_HEADSEAT, 'Две гарнитуры'),
    ]

    broadcast_start_date = models.DateTimeField(
        help_text='Broadcast start date and time(YYYY-MM-DD hh:mm)',
    )
    broadcast_end_date = models.DateTimeField(
        help_text='Broadcast end date and time(YYYY-MM-DD hh:mm)',
    )
    place = models.ForeignKey(
        PlaceConstructor,
        on_delete=models.CASCADE,
    )
    type = models.ForeignKey(
        BroadCastType, on_delete=models.CASCADE,
    )
    start_date = models.DateTimeField(
        help_text='Arrival date and time (YYYY-MM-DD hh:mm)',
        blank=True,
        null=True
    )
    end_date = models.DateTimeField(
        help_text='Departure date and time (YYYY-MM-DD hh:mm)',
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
        verbose_name='PTS configuration',
    )
    commentator_monitor = models.BooleanField(
        'Monitor for commentator',
        default=False
    )
    commentator_console = models.BooleanField(
        'Sound console for commentator',
        default=False
    )
    commentator_headset = models.CharField(
        verbose_name='Number of headsets',
        max_length=30,
        choices=HEADSEAT,
    )
    create_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    def get_absolute_url(self):
        return reverse('pts_requests:request_detail', kwargs={"pk": self.pk})

    def get_pts(self):
        return ", ".join([pts.name for pts in self.pts_name.all()])

    class Meta:
        verbose_name = 'PTS Request'
        verbose_name_plural = 'PTS Requests'
        ordering = ('broadcast_start_date', )
