# Generated by Django 3.0.4 on 2020-03-15 21:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ispitni_rokovi', '0008_vezasmerpredmet_godina_studija'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='VezaSmerPredmet',
            new_name='SmerPredmet',
        ),
    ]