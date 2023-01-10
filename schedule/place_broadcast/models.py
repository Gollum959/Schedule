from django.db import models


class PlaceConstructor(models.Model):
    name = models.CharField('PTS config name', max_length=30, unique=True)

    def __str__(self) -> str:
        return f'{self.name}'

    class Meta:
        verbose_name = 'Location of the broadcast'
        verbose_name_plural = 'Broadcast locations'
        ordering = ('id', )
