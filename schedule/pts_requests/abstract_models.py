from django.db import models


class NameModel(models.Model):
    """Abstract model with name."""
    name = models.CharField(max_length=200)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return f'{self.name}'
