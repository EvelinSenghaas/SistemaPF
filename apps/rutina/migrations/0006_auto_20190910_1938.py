# Generated by Django 2.2.5 on 2019-09-10 22:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rutina', '0005_auto_20190910_1039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rutina',
            name='profesor_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='home', to='home.Profesor'),
        ),
    ]
