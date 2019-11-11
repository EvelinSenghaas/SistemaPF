# Generated by Django 2.2.5 on 2019-11-11 17:57

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0052_auto_20191111_1456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fichaalumno',
            name='circunferenciaMuneca',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
