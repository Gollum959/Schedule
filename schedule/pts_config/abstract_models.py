from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class ConstrQuantity(models.Model):
    """Abstract model for PTS configuration"""

    constructor = models.ForeignKey(
        'PtsConstructor',
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveSmallIntegerField(
        'Quantity',
        validators=(
            MinValueValidator(0),
            MaxValueValidator(15),
        ),
        default=0
    )

    class Meta:
        abstract = True


class StrName(models.Model):
    """Abstract model for __str__ method"""
    def __str__(self) -> str:
        return f'{self.name}'

    class Meta:
        abstract = True
