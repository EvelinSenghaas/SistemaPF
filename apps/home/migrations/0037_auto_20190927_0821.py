# Generated by Django 2.2.5 on 2019-09-27 11:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0036_disponibilidadprofesor_alumno_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='disponibilidadprofesor',
            name='alumno_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.Alumno', verbose_name='Alumno'),
        ),
    ]
