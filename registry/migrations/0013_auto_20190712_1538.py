# Generated by Django 2.2.3 on 2019-07-12 15:38

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('registry', '0012_auto_20190710_1639'),
    ]

    operations = [
        migrations.RenameField(
            model_name='aircraft',
            old_name='begin_date',
            new_name='commission_date',
        ),
        migrations.AddField(
            model_name='aircraft',
            name='operating_frequencies',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='aircraft',
            name='sub_category',
            field=models.IntegerField(choices=[(0, 'Other'), (1, 'AIRPLANE'), (2, 'NONPOWERED GLIDER'), (3, 'POWERED GLIDER'), (4, 'HELICOPTER'), (5, 'GYROPLANE'), (6, 'BALLOON'), (6, 'AIRSHIP'), (7, 'UAV'), (8, 'Multirotor'), (9, 'Hybrid')], default=7),
        ),
        migrations.AlterField(
            model_name='authorization',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 12, 0, 0, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='operator',
            name='expiration',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 12, 0, 0, tzinfo=utc)),
        ),
    ]
