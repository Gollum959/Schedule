from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """User model."""

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLES = [
        (USER, 'USER'),
        (MODERATOR, 'MODERATOR'),
        (ADMIN, 'ADMINISTRATOR'),
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
