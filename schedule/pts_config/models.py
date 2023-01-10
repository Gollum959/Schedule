from django.db import models


class PtsConstructor(models.Model):
    name = models.CharField('PTS config name', max_length=30, unique=True)

    def __str__(self) -> str:
        return f'{self.name}'

    class Meta:
        verbose_name = 'PTS config'
        verbose_name_plural = 'PTS configs'
        ordering = ('id', )
