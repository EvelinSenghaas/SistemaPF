# Generated by Django 2.2.5 on 2019-09-09 15:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_auto_20190909_0925'),
    ]

    operations = [
        migrations.AddField(
            model_name='alumno',
            name='profesor_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='home.Profesor', verbose_name='Profesor'),
            preserve_default=False,
        ),
    ]