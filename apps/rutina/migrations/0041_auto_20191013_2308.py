# Generated by Django 2.2.5 on 2019-10-14 02:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rutina', '0040_auto_20191013_2306'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='revision',
            options={'get_latest_by': 'fechaRevision', 'ordering': ['fechaRevision'], 'verbose_name': 'Revision', 'verbose_name_plural': 'Revisiones'},
        ),
        migrations.AlterModelOptions(
            name='sesion',
            options={'get_latest_by': 'fechaSesion', 'ordering': ['fechaSesion'], 'verbose_name': 'Sesion', 'verbose_name_plural': 'Sesiones'},
        ),
    ]
