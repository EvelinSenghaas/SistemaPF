# Generated by Django 2.2.5 on 2019-09-08 12:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20190908_0944'),
        ('rutina', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rutina',
            name='profesor_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='home', to='home.Profesor'),
        ),
    ]
