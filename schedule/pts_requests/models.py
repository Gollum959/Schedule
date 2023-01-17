from django.db import models
from django.urls import reverse

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
        help_text='Broadcast date(YYYY-MM-DD)',
    )
    place = models.ForeignKey(
        PlaceConstructor,
        on_delete=models.CASCADE,
    )
    type = models.ForeignKey(
        BroadCastType, on_delete=models.CASCADE,
    )
    start_date = models.DateTimeField(
        help_text='Broadcast start date and time (YYYY-MM-DD hh:mm)',
    )
    end_date = models.DateTimeField(
        help_text='Broadcast end date and time (YYYY-MM-DD hh:mm)',
    )
    pts_name = models.ForeignKey(
        PtsName, on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    pts_cfg = models.ForeignKey(
        PtsConstructor,
        on_delete=models.CASCADE,
        verbose_name='PTS configuration',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    def get_absolute_url(self):
        return reverse('pts_requests:request_detail', kwargs={"pk": self.pk})

    class Meta:
        verbose_name = 'PTS Request'
        verbose_name_plural = 'PTS Requests'
        ordering = ('broadcast_date', )
