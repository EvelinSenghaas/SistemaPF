# Generated by Django 2.2.5 on 2019-09-23 11:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0027_auto_20190923_0758'),
    ]

    operations = [
        migrations.AlterField(
            model_name='disponibilidadprofesor',
            name='semana_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Semana', verbose_name='Dia'),
        ),
    ]