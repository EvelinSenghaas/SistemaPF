# Generated by Django 2.2.5 on 2019-09-08 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Actividad',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=60, null=True)),
                ('descripcion', models.TextField(null=True)),
                ('estado', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Actividad',
                'verbose_name_plural': 'Actividades',
                'ordering': ['nombre'],
                'permissions': (),
            },
        ),
        migrations.CreateModel(
            name='Detalle',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('atributo', models.CharField(max_length=30, null=True)),
                ('aspectoMejora', models.CharField(max_length=30, null=True)),
            ],
            options={
                'verbose_name': 'Detalle',
                'verbose_name_plural': 'Detalles',
                'ordering': ['atributo'],
            },
        ),
        migrations.CreateModel(
            name='Rutina',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=60, null=True)),
                ('descripcion', models.TextField(null=True)),
                ('estado', models.BooleanField(default=True)),
                ('actividad_id', models.ManyToManyField(to='rutina.Actividad', verbose_name='Actividad')),
            ],
            options={
                'verbose_name': 'Rutina',
                'verbose_name_plural': 'Rutinas',
                'ordering': ['nombre'],
            },
        ),
        migrations.AddField(
            model_name='actividad',
            name='detalle_id',
            field=models.ManyToManyField(to='rutina.Detalle', verbose_name='Detalle'),
        ),
    ]
