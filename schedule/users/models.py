from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """User model."""

    USER = 'user'
    MAIN_DIRECTOR = 'main_director'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLES = [
        (USER, 'Режиссёр'),
        (MAIN_DIRECTOR, 'Главный режисёр'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
    ]

    GPC = 'gpc'
    ATN = 'atn'
    BEL5 = 'bel5'
    DIRECTIONS = [
        (GPC, 'ГПЦ'),
        (ATN, 'АТН'),
        (BEL5, 'Беларусь 5'),
    ]

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)

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
    def is_admin_or_moderator(self):
        """Return True if user is Moderator or Admin."""
        return (self.role == self.MODERATOR or
                self.role == self.ADMIN or
                self.is_superuser
        )

    @property
    def is_main_director_or_admin(self):
        """Return True if user is Admin."""
        return (
            self.role == self.ADMIN or
            self.is_superuser or
            self.role == self.MAIN_DIRECTOR
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
