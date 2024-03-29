# Generated by Django 2.2.5 on 2019-09-14 14:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rutina', '0018_remove_actividad_nivel_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='repeticion',
            name='actividad_id',
        ),
        migrations.AddField(
            model_name='repeticion',
            name='actividad_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='rutina.Actividad', verbose_name='Actividad'),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='repeticion',
            name='nivel_id',
        ),
        migrations.AddField(
            model_name='repeticion',
            name='nivel_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='rutina.Nivel', verbose_name='Nivel'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='repeticion',
            name='repeticionesMinimas',
            field=models.PositiveIntegerField(verbose_name='Repeticiones Minimas'),
        ),
    ]
