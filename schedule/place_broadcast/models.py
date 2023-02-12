from django.db import models
from django.urls import reverse
from users.models import User


class PlaceCity(models.Model):
    name = models.CharField('City name', max_length=30)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return f'{self.name}'

    class Meta:
        unique_together = ('name', 'author',)


class PlaceConstructor(models.Model):
    """Broadcast address constructor"""
    name = models.CharField('Название Объекта', max_length=70)
    city_name = models.ForeignKey(
        'PlaceCity',
        on_delete=models.CASCADE,
    )
    address = models.CharField('Адрес', max_length=300)
    contact_name = models.CharField(
        'Name of person in charge at the facility',
        max_length=120,
    )
    phone = models.CharField('Contact phone', max_length=25, blank=True)
    web = models.URLField('Website Address', blank=True)
    email_address = models.EmailField('Email Address', blank=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('place:place_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Location of the broadcast'
        verbose_name_plural = 'Broadcast locations'
        ordering = ('create_date', )
