# Generated by Django 2.2.5 on 2019-09-09 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_alumno_profesor_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='FichaAlumno',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
    ]
