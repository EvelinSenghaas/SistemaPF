# Generated by Django 2.2.5 on 2019-10-04 01:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rutina', '0021_auto_20191002_1351'),
    ]

    operations = [
        migrations.CreateModel(
            name='EvaluacionNivel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('cantSesiones', models.PositiveIntegerField(verbose_name='Sesiones Minimas')),
                ('nivel_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='rutina.Nivel', verbose_name='Nivel')),
            ],
        ),
    ]
