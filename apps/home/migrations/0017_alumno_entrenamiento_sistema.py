# Generated by Django 2.2.5 on 2019-09-20 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0016_auto_20190918_1410'),
    ]

    operations = [
        migrations.AddField(
            model_name='alumno',
            name='entrenamiento_sistema',
            field=models.BooleanField(default=None),
        ),
    ]