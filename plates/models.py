from django.db import models
from commons.models import TimeStampedModel
from meals.models import Meal


class Plate(TimeStampedModel):
    '''
    Plate model that can include several meals, for example, desserts,
    deep plate and others
    '''
    name = models.CharField(
        verbose_name='Nombre',
        max_length=200
    )
    meals = models.ManyToManyField(
        Meal,
        verbose_name='Comidas',
        related_name='plates'
    )
    owner = models.ForeignKey(
        'users.User',
        related_name='plate',
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name
