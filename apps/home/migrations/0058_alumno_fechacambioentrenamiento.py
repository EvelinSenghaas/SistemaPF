# Generated by Django 2.2.5 on 2019-11-25 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0057_auto_20191111_1723'),
    ]

    operations = [
        migrations.AddField(
            model_name='alumno',
            name='fechaCambioEntrenamiento',
            field=models.DateField(blank=True, null=True),
        ),
    ]
