# Generated by Django 3.1.3 on 2020-11-30 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gcs_operations', '0013_auto_20201130_1328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flightoperation',
            name='name',
            field=models.CharField(default='Flight Operation iadltb', max_length=30),
        ),
        migrations.AlterField(
            model_name='flightplan',
            name='name',
            field=models.CharField(default='Flight Plan jkxljk', max_length=30),
        ),
    ]
