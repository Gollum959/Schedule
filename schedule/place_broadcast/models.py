from django.db import models
from django.urls import reverse
from users.models import User


class PlaceCity(models.Model):
    """City model."""
    name = models.CharField('City name', unique=True, max_length=30)

    def __str__(self) -> str:
        return f'{self.name}'


class EventType(models.Model):
    """Event type model."""

    GPC = 'gpc'
    ATN = 'atn'
    BEL5 = 'bel5'
    DIRECTIONS = [
        (GPC, 'ГПЦ'),
        (ATN, 'АТН'),
        (BEL5, 'Беларусь 5'),
    ]

    name = models.CharField('Event type name', max_length=50)
    direction = models.CharField(
        verbose_name='User direction',
        max_length=15,
        choices=DIRECTIONS,
        default=BEL5,
        help_text='The direction of Belteleradiocompany'
    )

    def __str__(self) -> str:
        return f'{self.name}'

    class Meta:
        ordering = ('name', )


class PlaceConstructor(models.Model):
    """Broadcast address constructor."""

    name = models.CharField('Название Объекта', max_length=70)
    city_name = models.ForeignKey(
        'PlaceCity',
        on_delete=models.CASCADE,
    )
    event_type = models.ManyToManyField(
        'EventType',
        verbose_name='Виды событий',
    )
    address = models.CharField('Адрес', max_length=300)
    contact_name = models.CharField(
        'ФИО ответственного лица на объекте',
        max_length=120,
    )
    phone = models.CharField('Контактный телефон', max_length=25, blank=True)
    web = models.URLField('Website Address', blank=True)
    email_address = models.EmailField('E-mail', blank=True)
    judge_system = models.CharField(
        'Судейская система',
        max_length=150,
        blank=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('place:place_detail', kwargs={'pk': self.pk})

    @property
    def get_events(self):
        """Returns a string with all event_types that the site has"""

        return ", ".join([event.name for event in self.event_type.all()])

    class Meta:
        verbose_name = 'Location of the broadcast'
        verbose_name_plural = 'Broadcast locations'
        ordering = ('name', )
        constraints = [
            models.UniqueConstraint(
                fields=('name', 'city_name', 'author', ),
                name='one_place_in_city_author'
            )
        ]
