from django.db import models
from commons.models import TimeStampedModel


class Distribution(TimeStampedModel):
    """A model of a distribution place"""
    name = models.CharField(
        verbose_name='name',
        max_length=200,
        blank=False
    )
    link_id = models.CharField(
        verbose_name='Link de envío',
        max_length=200,
        help_text='Example: https://hooks.slack.com/services/*LINK*',
        blank=False
    )
    is_active = models.BooleanField(
        default=False
    )
    distribution_hour_link = models.TimeField(
        verbose_name='Hora de envío del link'
    )

    end_available_distribution_link = models.TimeField(
        verbose_name='Hora final de pedidos'
    )

    owner = models.ForeignKey(
        'users.User',
        related_name='distribution',
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name
