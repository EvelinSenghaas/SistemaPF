# Generated by Django 2.2.5 on 2019-10-04 01:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rutina', '0022_evaluacionnivel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluacionnivel',
            name='nivel_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rutina.Nivel', verbose_name='Nivel'),
        ),
    ]
