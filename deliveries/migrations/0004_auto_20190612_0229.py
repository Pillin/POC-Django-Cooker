# Generated by Django 2.2.1 on 2019-06-12 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deliveries', '0003_deliveryselection'),
    ]

    operations = [
        migrations.AlterField(
            model_name='delivery',
            name='hour_sent',
            field=models.TimeField(null=True),
        ),
    ]
