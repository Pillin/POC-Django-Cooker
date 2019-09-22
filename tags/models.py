from django.db import models
from commons.models import TimeStampedModel


class Tag(TimeStampedModel):
    name = models.CharField(
        verbose_name='Nombre',
        max_length=200,
        blank=False
    )
    owner = models.ForeignKey(
        'users.User',
        related_name='tag',
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name
