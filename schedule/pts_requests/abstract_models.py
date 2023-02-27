from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class NameModel(models.Model):
    """Abstract model with name."""
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return f'{self.name}'

    class Meta:
        abstract = True


class LineConstructor(models.Model):
    """Abstract model for commline."""

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
            MinValueValidator(1),
            MaxValueValidator(25),
        ),
        default=0,
    )

    pts_request = models.ForeignKey(
        'PtsRequest',
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True
