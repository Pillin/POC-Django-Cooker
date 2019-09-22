import uuid
import datetime
from django.db import models
from commons.models import TimeStampedModel
from distributions.models import Distribution
from menus.models import Menu
from plates.models import Plate


class Delivery(TimeStampedModel):
    distribution = models.ForeignKey(
        Distribution,
        related_name='deliveries',
        on_delete=models.CASCADE
    )
    menu = models.ForeignKey(
        Menu,
        related_name='deliveries',
        on_delete=models.CASCADE
    )
    date = models.DateField()
    hour_sent = models.TimeField(null=True)
    was_sending = models.BooleanField(
        default=False
    )
    menu_delivery_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    owner = models.ForeignKey(
        'users.User',
        related_name='delivery',
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ('menu_delivery_id',)

    def __str__(self):
        return ''

    def is_finished_booking(self):
        date = datetime.datetime.now()
        distribution_time = self.distribution.end_available_distribution_link
        return date.time() > distribution_time and datetime.date.today() <= self.date


class DeliverySelection(TimeStampedModel):
    delivery = models.ForeignKey(
        Delivery,
        related_name='delivery_selection',
        on_delete=models.CASCADE
    )
    plates = models.ManyToManyField(
        Plate,
        verbose_name='Platos',
        related_name='delivery'
    )
    description = models.CharField(
        verbose_name='Comentarios',
        max_length=200
    )
    name = models.CharField(
        verbose_name='Nombre',
        max_length=200
    )
    owner = models.ForeignKey(
        'users.User',
        related_name='delivery_selection',
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):

        return "{} {} \t{} {}".format(
            self.delivery.date,
            self.name,
            ','.join(self.plates.all().values_list('name', flat=True)),
            self.description
        )
