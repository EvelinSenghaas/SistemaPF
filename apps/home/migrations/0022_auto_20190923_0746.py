# Generated by Django 2.2.5 on 2019-09-23 10:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0021_semana_dia'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='semana',
            options={'ordering': ['dia'], 'verbose_name': 'Semana', 'verbose_name_plural': 'Semana'},
        ),
    ]