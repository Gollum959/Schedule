from django.db import models

from users.models import User


class tjkRequest(models.Model):

    name = models.CharField(
        'Название заявки ТЖК',
        max_length=50,
    )
    create_date = models.DateTimeField(auto_now_add=True)
    work_time_start = models.DateTimeField(
        verbose_name='Дата и время начала работ',
        help_text='Дата и время начала работ(YYYY-MM-DD hh:mm)',
    )
    work_time_end = models.DateTimeField(
        verbose_name='Дата и время окончания работ',
        help_text='Дата и время окончания работ(YYYY-MM-DD hh:mm)',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
