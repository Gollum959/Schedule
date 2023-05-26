from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """User model."""

    USER = 'user'
    MAIN_DIRECTOR = 'main_director'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    SOUNDMAN = 'soundman'
    GDPT = 'gdpt'
    DTOV_HEADMASTER = 'headmaster'
    ROLES = [
        (USER, 'Режиссёр'),
        (MAIN_DIRECTOR, 'Главный режисёр'),
        (SOUNDMAN, 'Звукорежиссёр'),
        (MODERATOR, 'Начальник цеха ПТС'),
        (ADMIN, 'Администратор'),
        (GDPT, 'Директор ГДПТ'),
        (DTOV_HEADMASTER, 'Директор ДТОВ'),
    ]

    GPC = 'gpc'
    ATN = 'atn'
    BEL5 = 'bel5'
    DTOV = 'dtov'
    DIRECTIONS = [
        (GPC, 'ГПЦ'),
        (ATN, 'АТН'),
        (BEL5, 'Беларусь 5'),
        (DTOV, 'ДТОВ'),
        (GDPT, 'ГДПТ'),
    ]

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    surname = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )

    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    direction = models.CharField(
        verbose_name='User direction',
        max_length=15,
        choices=DIRECTIONS,
        default=BEL5,
        help_text='The direction of Belteleradiocompany'
    )

    position = models.CharField(
        max_length=50,
        help_text='User position in the direction'
    )
    role = models.CharField(
        verbose_name='User role',
        max_length=15,
        choices=ROLES,
        default=USER,
        help_text='The rights that the user has'
    )

    class Meta:
        ordering = ('id', )

    @property
    def is_admin(self):
        """Return True if user is Admin."""
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        """Return True if user is Moderator."""
        return self.role == self.MODERATOR

    @property
    def is_soundman(self):
        """Return True if user is Moderator."""
        return self.role == self.SOUNDMAN

    @property
    def is_gdpt(self):
        """Return True if user is GDPT."""
        return self.role == self.GDPT

    @property
    def is_dtov_headmaster(self):
        """Return True if user is DTOV_HEADMASTER."""
        return self.role == self.DTOV_HEADMASTER

    @property
    def is_admin_or_moderator(self):
        """Return True if user is Moderator or Admin."""
        return (self.role == self.MODERATOR or
                self.role == self.ADMIN or
                self.is_superuser)

    @property
    def is_main_director_or_admin(self):
        """Return True if user is main director or admin."""
        return (
            self.role == self.ADMIN or
            self.is_superuser or
            self.role == self.MAIN_DIRECTOR
        )

    @property
    def is_gdpt_or_admin(self):
        """Return True if user is gdpt or admin."""
        return (
            self.role == self.ADMIN or
            self.is_superuser or
            self.role == self.GDPT
        )

    @property
    def is_dtov_headmaster_or_admin(self):
        """Return True if user is gdpt or admin."""
        return (
            self.role == self.ADMIN or
            self.is_superuser or
            self.role == self.DTOV_HEADMASTER
        )

    @property
    def is_soundman_or_admin(self):
        """Return True if user is soundman or admin."""
        return (
            self.role == self.ADMIN or
            self.role == self.SOUNDMAN
        )

    @property
    def is_main_director(self):
        """Return True if user is Admin."""
        return (
            self.role == self.MAIN_DIRECTOR
        )

    @property
    def is_director(self):
        """Return True if user is Admin."""
        return (
            self.role == self.USER
        )

    @property
    def get_fio(self):
        """Return FIO."""
        short_surname = f'{self.surname}' if self.surname else ''

        return f'{self.last_name} {self.first_name} {short_surname}'
