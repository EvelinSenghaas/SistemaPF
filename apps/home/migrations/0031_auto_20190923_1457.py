# Generated by Django 2.2.5 on 2019-09-23 17:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0030_disponibilidadprofesor_horario_final'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='disponibilidadprofesor',
            options={'ordering': ['horario_inicio'], 'verbose_name': 'Disponibilidad Profesor', 'verbose_name_plural': 'Disponibilidad Profesor'},
        ),
        migrations.RenameField(
            model_name='disponibilidadprofesor',
            old_name='horario',
            new_name='horario_inicio',
        ),
    ]
