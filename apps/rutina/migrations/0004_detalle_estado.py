# Generated by Django 2.2.5 on 2019-09-10 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rutina', '0003_actividad_nivel_exigencia'),
    ]

    operations = [
        migrations.AddField(
            model_name='detalle',
            name='estado',
            field=models.BooleanField(default=True),
        ),
    ]
