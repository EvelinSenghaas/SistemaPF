# Generated by Django 2.2.5 on 2019-11-01 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rutina', '0059_auto_20191031_0852'),
    ]

    operations = [
        migrations.AlterField(
            model_name='revisionsesion',
            name='pesoActual',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Peso anterior'),
        ),
        migrations.AlterField(
            model_name='revisionsesion',
            name='pesoRevision',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Peso revision'),
        ),
    ]
