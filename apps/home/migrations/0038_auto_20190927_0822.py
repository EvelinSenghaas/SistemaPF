# Generated by Django 2.2.5 on 2019-09-27 11:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0037_auto_20190927_0821'),
    ]

    operations = [
        migrations.AlterField(
            model_name='disponibilidadprofesor',
            name='alumno_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.Alumno', verbose_name='Alumno'),
        ),
    ]
