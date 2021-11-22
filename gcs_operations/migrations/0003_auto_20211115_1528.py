# Generated by Django 3.2.9 on 2021-11-15 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gcs_operations', '0002_flightplan_geo_json'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flightplan',
            name='kml',
        ),
        migrations.AddField(
            model_name='flightplan',
            name='plan_file_json',
            field=models.JSONField(default=dict, help_text='Paste the QGCS flight plan JSON, for more information about the Plan File Format see: https://dev.qgroundcontrol.com/master/en/file_formats/plan.html'),
        ),
    ]