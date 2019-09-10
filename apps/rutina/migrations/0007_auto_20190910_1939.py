# Generated by Django 2.2.5 on 2019-09-10 22:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rutina', '0006_auto_20190910_1938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actividad',
            name='detalle_id',
            field=models.ManyToManyField(blank=True, to='rutina.Detalle', verbose_name='Detalle'),
        ),
        migrations.AlterField(
            model_name='rutina',
            name='profesor_id',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, related_name='home', to='home.Profesor'),
            preserve_default=False,
        ),
    ]
