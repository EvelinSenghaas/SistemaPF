# Generated by Django 2.2.5 on 2019-10-31 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rutina', '0057_auto_20191031_0838'),
    ]

    operations = [
        migrations.AlterField(
            model_name='revisionsesion',
            name='fechaRevision',
            field=models.DateField(auto_now=True, null=True, verbose_name='Fecha de revision'),
        ),
    ]
