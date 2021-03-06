# Generated by Django 2.2.1 on 2019-06-11 05:33

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('distributions', '0004_distribution_distribution_hour_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='distribution',
            name='end_available_distribution_link',
            field=models.TimeField(default=datetime.datetime(2019, 6, 11, 5, 33, 15, 171894, tzinfo=utc), verbose_name='Hora final de pedidos'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='distribution',
            name='distribution_hour_link',
            field=models.TimeField(verbose_name='Hora de envío del link'),
        ),
        migrations.AlterField(
            model_name='distribution',
            name='link_id',
            field=models.CharField(max_length=200, verbose_name='Link de envío'),
        ),
        migrations.AlterField(
            model_name='distribution',
            name='name',
            field=models.CharField(max_length=200, verbose_name='name'),
        ),
    ]
