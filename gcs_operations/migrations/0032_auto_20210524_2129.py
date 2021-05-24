# Generated by Django 3.2.3 on 2021-05-24 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gcs_operations', '0031_auto_20210506_1209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flightoperation',
            name='name',
            field=models.CharField(default='Medicine Delivery Operation', max_length=30),
        ),
        migrations.AlterField(
            model_name='flightplan',
            name='geo_json',
            field=models.TextField(default='{"type":"FeatureCollection","features":[]}', help_text='Paste flight plan geometry as GeoJSON'),
        ),
        migrations.AlterField(
            model_name='flightplan',
            name='name',
            field=models.CharField(default='Delivery Plan', help_text='Give this flight plan a friendly name', max_length=30),
        ),
    ]
