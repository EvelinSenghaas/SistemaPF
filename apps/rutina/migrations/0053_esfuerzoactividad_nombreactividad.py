# Generated by Django 2.2.5 on 2019-10-25 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rutina', '0052_auto_20191025_0835'),
    ]

    operations = [
        migrations.AddField(
            model_name='esfuerzoactividad',
            name='nombreActividad',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
    ]