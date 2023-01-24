from django.db import models


class NameModel(models.Model):
    """Abstract model with name."""
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return f'{self.name}'

    class Meta:
        abstract = True


class LineConstructor(models.Model):
    """Abstract model for direction."""
    DIRECTION_TO = 'to_pts'
    DIRECTION_FROM = 'from_pts'
    DIRECTION = [
        (DIRECTION_TO, 'От ЦА к ПТС'),
        (DIRECTION_FROM, 'От ПТС к ЦА'),
    ]
    direction = models.CharField(
        verbose_name='Direction',
        max_length=20,
        choices=DIRECTION,
    )
    pts_request = models.ForeignKey(
        'PtsRequest',
        on_delete=models.CASCADE,
    )

    @property
    def str_directions(self):
        return 'От ПТС к ЦА' if self.direction == 'from_pts' else 'От ЦА к ПТС'

    class Meta:
        abstract = True
