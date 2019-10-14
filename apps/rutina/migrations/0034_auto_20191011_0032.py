# Generated by Django 2.2.5 on 2019-10-11 03:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rutina', '0033_auto_20191009_1213'),
    ]

    operations = [
        migrations.AddField(
            model_name='sesion',
            name='descripcion',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sesion',
            name='esfuerzoSesion',
            field=models.IntegerField(default=1, verbose_name='Costo de sesión'),
            preserve_default=False,
        ),
    ]
