# Generated by Django 2.2.5 on 2019-10-25 03:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rutina', '0046_remove_revision_descripcion'),
    ]

    operations = [
        migrations.CreateModel(
            name='EsfuerzoActividad',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('esfuerzoActividad', models.IntegerField(blank=True, null=True, verbose_name='Costo de actividad')),
                ('actividad_id', models.ManyToManyField(blank=True, null=True, to='rutina.Actividad', verbose_name='Actividad')),
                ('sesion_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rutina.Sesion')),
            ],
            options={
                'verbose_name': 'Esfuerzo de actividad',
                'verbose_name_plural': 'Esfuerzos de actividades',
                'ordering': ['id'],
            },
        ),
    ]
