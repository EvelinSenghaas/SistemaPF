# Generated by Django 2.2.5 on 2019-09-23 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0019_disponibilidadprofesor_semana'),
    ]

    operations = [
        migrations.AlterField(
            model_name='semana',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]