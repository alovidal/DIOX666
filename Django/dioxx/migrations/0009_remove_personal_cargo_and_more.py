# Generated by Django 5.0.6 on 2024-10-26 16:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dioxx', '0008_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='personal',
            name='cargo',
        ),
        migrations.RemoveField(
            model_name='detallereceta',
            name='idMedicamento',
        ),
        migrations.RemoveField(
            model_name='detallereceta',
            name='idReceta',
        ),
        migrations.RemoveField(
            model_name='emergencia',
            name='residente',
        ),
        migrations.RemoveField(
            model_name='receta',
            name='residente',
        ),
        migrations.DeleteModel(
            name='cargoPersonal',
        ),
        migrations.DeleteModel(
            name='personal',
        ),
        migrations.DeleteModel(
            name='medicamento',
        ),
        migrations.DeleteModel(
            name='detalleReceta',
        ),
        migrations.DeleteModel(
            name='emergencia',
        ),
        migrations.DeleteModel(
            name='receta',
        ),
        migrations.DeleteModel(
            name='residente',
        ),
    ]
