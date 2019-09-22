from django.db import models
from commons.models import TimeStampedModel
from tags.models import Tag


class Meal(TimeStampedModel):
    name = models.CharField(
        verbose_name='Nombre',
        max_length=200,
        blank=False
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Etiquetas',
        blank=True,
        related_name='meals'
    )
    owner = models.ForeignKey(
        'users.User',
        related_name='meal',
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return "[{}] {}".format(",".join(self.get_tags()), self.name)

    def get_tags(self):
        return self.tags.values_list('name', flat=True)
