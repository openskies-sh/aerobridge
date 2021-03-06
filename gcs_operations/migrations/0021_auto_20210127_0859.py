# Generated by Django 3.1.5 on 2021-01-27 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gcs_operations', '0020_auto_20210126_2143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flightoperation',
            name='name',
            field=models.CharField(default='Flight Operation ruxwfl', max_length=30),
        ),
        migrations.AlterField(
            model_name='flightplan',
            name='details',
            field=models.TextField(help_text='Paste flight plan geometry', null=True),
        ),
        migrations.AlterField(
            model_name='flightplan',
            name='name',
            field=models.CharField(default='Flight Plan fxaury', max_length=30),
        ),
    ]
