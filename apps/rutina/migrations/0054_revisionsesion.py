# Generated by Django 2.2.5 on 2019-10-31 11:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0048_auto_20191028_1729'),
        ('rutina', '0053_esfuerzoactividad_nombreactividad'),
    ]

    operations = [
        migrations.CreateModel(
            name='RevisionSesion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fechaRevision', models.DateField(auto_now=True, verbose_name='Fecha de revision')),
                ('nivelAnterior', models.CharField(max_length=60, unique=True, verbose_name='Nivel anterior')),
                ('nivelRevision', models.CharField(max_length=60, unique=True, verbose_name='Nivel revision')),
                ('revisado', models.BooleanField(default=True)),
                ('comentario', models.TextField(null=True)),
                ('alumno_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='homeARS', to='home.Alumno')),
                ('profesor_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='homePRS', to='home.Profesor')),
                ('sesion_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rutina.Sesion')),
            ],
        ),
    ]