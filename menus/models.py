from datetime import datetime, timedelta
from deliveries.celery import call_send_link_task
from django.db import models
from commons.models import TimeStampedModel
from plates.models import Plate


class Menu(TimeStampedModel):
    '''
    Model for create the menu, with a name and diferent plates
    '''
    name = models.CharField(
        verbose_name='Nombre',
        max_length=200,
        blank=False
    )
    plates = models.ManyToManyField(
        Plate,
        verbose_name='Platos',
        related_name='menus'
    )
    owner = models.ForeignKey(
        'users.User',
        related_name='menu',
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        date = map(
            lambda elem: elem.strftime('%d-%m-%Y'),
            self.deliveries.all().values_list('date', flat=True))
        return "{} {} {}".format(
            self.name,
            [str(','.join(date))],
            ",".join(self.plates.all().values_list('name', flat=True))
        )

    def send_slack_link(self):
        '''
           build time and information for sending to slack
        '''
        delivery = self.deliveries.first()
        distribution = delivery.distribution

        delta = datetime(
            year=delivery.date.year,
            month=delivery.date.month,
            day=delivery.date.day,
            hour=distribution.distribution_hour_link.hour,
            minute=distribution.distribution_hour_link.minute
        )
        try:
            call_send_link_task.apply_async(
                args=(distribution.link_id, str(delivery.menu_delivery_id)),
                eta=delta + timedelta(hours=4)
            )
        except OSError:
            print("Celery is down")
