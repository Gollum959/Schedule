from django.db import models


class PlaceConstructor(models.Model):
    """Broadcast address constructor"""
    name = models.CharField('Name of the facility', max_length=30, unique=True)
    city = models.CharField('City', max_length=30)
    address = models.CharField('Address', max_length=300)
    contact_name = models.CharField('Name of person in charge at the facility', max_length=120)
    phone = models.CharField('Contact phone', max_length=25, blank=True)
    web = models.URLField('Website Address', blank=True)
    email_address = models.EmailField('Email Address', blank=True)

    def __str__(self) -> str:
        return f'{self.name}'

    class Meta:
        verbose_name = 'Location of the broadcast'
        verbose_name_plural = 'Broadcast locations'
        ordering = ('id', )
