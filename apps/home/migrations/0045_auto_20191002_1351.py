# Generated by Django 2.2.5 on 2019-10-02 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0044_auto_20191002_1011'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='semana',
            options={'ordering': ['numero'], 'verbose_name': 'Semana', 'verbose_name_plural': 'Semana'},
        ),
        migrations.AlterField(
            model_name='alumno',
            name='nombre',
            field=models.CharField(max_length=60, null=True, verbose_name='Nombre'),
        ),
    ]