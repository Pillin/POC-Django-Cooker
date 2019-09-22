# Generated by Django 2.2.1 on 2019-06-08 14:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('distributions', '0001_initial'),
        ('menus', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('date', models.DateField()),
                ('hour_sent', models.TimeField()),
                ('was_sending', models.BooleanField(default=False)),
                ('distribution', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='deliveries', to='distributions.Distribution')),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='deliveries', to='menus.Menu')),
            ],
            options={
                'ordering': ('id',),
            },
        ),
    ]
