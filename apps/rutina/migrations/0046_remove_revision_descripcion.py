# Generated by Django 2.2.5 on 2019-10-25 02:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rutina', '0045_revision_descripcion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='revision',
            name='descripcion',
        ),
    ]
