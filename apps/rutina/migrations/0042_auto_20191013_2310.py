# Generated by Django 2.2.5 on 2019-10-14 02:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rutina', '0041_auto_20191013_2308'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='revision',
            name='alumno_id',
        ),
        migrations.AddField(
            model_name='revision',
            name='sesion_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='rutina.Sesion'),
            preserve_default=False,
        ),
    ]