# Generated by Django 2.2.5 on 2019-11-08 03:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rutina', '0060_auto_20191101_1026'),
    ]

    operations = [
        migrations.AddField(
            model_name='esfuerzoactividad',
            name='nivel_id',
            field=models.CharField(blank=True, max_length=60, null=True, verbose_name='Nivel de sesion'),
        ),
    ]
