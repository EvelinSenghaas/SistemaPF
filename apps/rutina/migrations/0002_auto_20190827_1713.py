# Generated by Django 2.2.4 on 2019-08-27 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rutina', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Actividad',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=60)),
                ('descripcion', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='rutina',
            name='nombre',
            field=models.CharField(max_length=60),
        ),
    ]
