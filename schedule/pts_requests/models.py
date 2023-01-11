from django.db import models

from users.models import User
from pts_config.models import PtsConstructor
from place_broadcast.models import PlaceConstructor
from pts_requests.abstract_models import NameModel


class BroadCastType(NameModel):
    """Type of the broadcast(live, recording, test)"""


class PtsName(NameModel):
    """Names of PTS"""


class PtsRequest(models.Model):
    """Broadcast request model."""

    broadcast_date = models.DateField(
        help_text='Broadcast date',
    )
    place = models.ForeignKey(
        PlaceConstructor,
        on_delete=models.CASCADE,
    )
    type = models.ForeignKey(
        BroadCastType, on_delete=models.CASCADE,
    )
    start_date = models.DateTimeField(
        help_text='Broadcast start date and time',
    )
    end_date = models.DateTimeField(
        help_text='Broadcast end date and time',
    )
    pts_name = models.ForeignKey(
        PtsName, on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    pts_cfg = models.ForeignKey(
        PtsConstructor,
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'PTS Request'
        verbose_name_plural = 'PTS Requests'
        ordering = ('broadcast_date', )
