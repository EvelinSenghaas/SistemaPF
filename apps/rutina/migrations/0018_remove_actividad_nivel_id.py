# Generated by Django 2.2.5 on 2019-09-14 13:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rutina', '0017_auto_20190914_1046'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='actividad',
            name='nivel_id',
        ),
    ]