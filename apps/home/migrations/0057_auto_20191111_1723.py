# Generated by Django 2.2.5 on 2019-11-11 20:23

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0056_auto_20191111_1722'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fichaalumno',
            name='altura',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(3)]),
        ),
    ]
