# Generated by Django 2.2.3 on 2019-07-10 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registry', '0011_auto_20190710_1153'),
    ]

    operations = [
        migrations.RenameField(
            model_name='aircraft',
            old_name='image',
            new_name='identification_photo',
        ),
        migrations.RenameField(
            model_name='aircraft',
            old_name='image_small',
            new_name='identification_photo_small',
        ),
        migrations.AddField(
            model_name='aircraft',
            name='photo',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='aircraft',
            name='photo_small',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='pilot',
            name='identification_photo',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='pilot',
            name='identificationiphoto_small',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='pilot',
            name='photo',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='pilot',
            name='photo_small',
            field=models.URLField(blank=True, null=True),
        ),
    ]
